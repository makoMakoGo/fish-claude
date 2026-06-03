from __future__ import annotations

import importlib.util
import json
import os
import sys
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MIGRATOR_PATH = Path(__file__).resolve().with_name("migrate.py")
spec = importlib.util.spec_from_file_location("codex_provider_history_migrator", MIGRATOR_PATH)
assert spec is not None
migrator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = migrator
assert spec.loader is not None
spec.loader.exec_module(migrator)


KEEP_OPENAI = {"openai"}


def rollout_line(provider: str) -> str:
    return json.dumps(
        {
            "timestamp": "2026-05-24T00:00:00.000Z",
            "type": "session_meta",
            "payload": {
                "id": "session-id",
                "timestamp": "2026-05-24T00:00:00.000Z",
                "cwd": "/tmp",
                "originator": "codex-tui",
                "cli_version": "0.134.0-alpha.1",
                "source": "cli",
                "model_provider": provider,
            },
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def event_line() -> str:
    return json.dumps(
        {
            "timestamp": "2026-05-24T00:00:01.000Z",
            "type": "event_msg",
            "payload": {"type": "task_started", "turn_id": "turn-id"},
        },
        separators=(",", ":"),
    )


def create_threads_db(path: Path, providers: list[str | None]) -> None:
    conn = sqlite3.connect(path)
    try:
        conn.execute("CREATE TABLE threads (id TEXT PRIMARY KEY, model_provider TEXT)")
        conn.executemany(
            "INSERT INTO threads (id, model_provider) VALUES (?, ?)",
            [(f"thread-{index}", provider) for index, provider in enumerate(providers)],
        )
        conn.commit()
    finally:
        conn.close()


def db_providers(path: Path) -> list[tuple[str | None, int]]:
    conn = sqlite3.connect(path)
    try:
        return conn.execute(
            "SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider ORDER BY COUNT(*) DESC, model_provider ASC"
        ).fetchall()
    finally:
        conn.close()


class ProviderDecisionTests(unittest.TestCase):
    def test_should_migrate_provider_keeps_openai_and_missing_values(self) -> None:
        self.assertFalse(migrator.should_migrate_provider("openai", KEEP_OPENAI))
        self.assertFalse(migrator.should_migrate_provider(None, KEEP_OPENAI))
        self.assertFalse(migrator.should_migrate_provider("", KEEP_OPENAI))

    def test_should_migrate_provider_migrates_non_empty_custom_provider(self) -> None:
        self.assertTrue(migrator.should_migrate_provider("custom-provider", KEEP_OPENAI))


class RolloutRewriteTests(unittest.TestCase):
    def test_dry_run_reports_migration_without_writing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp)
            path = codex_home / "sessions" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            original = f"{rollout_line('custom')}\n{event_line()}\n"
            path.write_text(original, encoding="utf-8")
            report = migrator.RolloutReport()

            migrator.rewrite_rollout_file(
                path=path,
                codex_home=codex_home,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=False,
                backup_root=None,
                report=report,
            )

            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertEqual(report.files_scanned, 1)
            self.assertEqual(report.files_needing_update, 1)
            self.assertEqual(report.files_updated, 0)
            self.assertEqual(report.session_meta_rewritten, 1)
            self.assertEqual(report.provider_counts_before, {"custom": 1})
            self.assertEqual(report.provider_counts_after, {"openai": 1})

    def test_apply_only_rewrites_session_meta_provider_and_keeps_other_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp)
            path = codex_home / "sessions" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            non_session_meta = event_line()
            path.write_text(f"{rollout_line('custom')}\n{non_session_meta}\n", encoding="utf-8")
            report = migrator.RolloutReport()

            migrator.rewrite_rollout_file(
                path=path,
                codex_home=codex_home,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=None,
                report=report,
            )

            lines = path.read_text(encoding="utf-8").splitlines()
            session_meta = json.loads(lines[0])
            self.assertEqual(session_meta["payload"]["model_provider"], "openai")
            self.assertEqual(lines[1], non_session_meta)
            self.assertEqual(report.files_updated, 1)

    def test_malformed_jsonl_is_skipped_and_valid_lines_still_migrate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp)
            path = codex_home / "sessions" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            malformed_line = '{"type":"response_item","payload":{"text":"unterminated'
            path.write_text(f"{malformed_line}\n{rollout_line('custom')}\n", encoding="utf-8")
            report = migrator.RolloutReport()

            migrator.rewrite_rollout_file(
                path=path,
                codex_home=codex_home,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=None,
                report=report,
            )

            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], malformed_line)
            self.assertEqual(json.loads(lines[1])["payload"]["model_provider"], "openai")
            self.assertEqual(report.parse_errors, 1)
            self.assertEqual(len(report.parse_error_locations), 1)
            self.assertIn("rollout.jsonl:1", report.parse_error_locations[0])
            self.assertEqual(report.files_updated, 1)

    def test_session_meta_payload_must_be_object(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp)
            path = codex_home / "sessions" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps({"type": "session_meta", "payload": "not-an-object"}) + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "session_meta payload 非对象"):
                migrator.rewrite_rollout_file(
                    path=path,
                    codex_home=codex_home,
                    target_provider="openai",
                    keep_providers=KEEP_OPENAI,
                    apply=False,
                    backup_root=None,
                    report=migrator.RolloutReport(),
                )

    def test_apply_preserves_newline_at_eof(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp)
            path = codex_home / "sessions" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            path.write_text(f"{rollout_line('custom')}\n", encoding="utf-8")

            migrator.rewrite_rollout_file(
                path=path,
                codex_home=codex_home,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=None,
                report=migrator.RolloutReport(),
            )

            self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))

    def test_apply_preserves_missing_newline_at_eof(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            codex_home = Path(temp)
            path = codex_home / "sessions" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            path.write_text(rollout_line("custom"), encoding="utf-8")

            migrator.rewrite_rollout_file(
                path=path,
                codex_home=codex_home,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=None,
                report=migrator.RolloutReport(),
            )

            self.assertFalse(path.read_text(encoding="utf-8").endswith("\n"))


class SqliteMigrationTests(unittest.TestCase):
    def test_dry_run_simulates_counts_without_updating_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            db_path = Path(temp) / "state_5.sqlite"
            create_threads_db(db_path, ["openai", "custom", "custom", None])

            report = migrator.migrate_sqlite(
                db_path=db_path,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=False,
                backup_root=None,
            )

            self.assertEqual(db_providers(db_path), [("custom", 2), (None, 1), ("openai", 1)])
            self.assertEqual(report.rows_needing_update, 2)
            self.assertEqual(report.rows_updated, 0)
            self.assertEqual(report.provider_counts_before, [("custom", 2), (None, 1), ("openai", 1)])
            self.assertEqual(report.provider_counts_after, [("openai", 3), (None, 1)])

    def test_apply_updates_only_non_keep_provider_and_preserves_null(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            db_path = Path(temp) / "state_5.sqlite"
            create_threads_db(db_path, ["openai", "custom", "custom", None])

            report = migrator.migrate_sqlite(
                db_path=db_path,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=None,
            )

            self.assertEqual(db_providers(db_path), [("openai", 3), (None, 1)])
            self.assertEqual(report.rows_needing_update, 2)
            self.assertEqual(report.rows_updated, 2)
            self.assertEqual(report.provider_counts_after, [("openai", 3), (None, 1)])


class StateDbResolutionTests(unittest.TestCase):
    def test_state_db_resolution_prefers_config_sqlite_home_then_env_then_codex_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            codex_home = root / "codex-home"
            env_home = root / "env-home"
            config_home = root / "config-home"
            for directory in (codex_home, env_home, config_home):
                directory.mkdir()
                (directory / "state_5.sqlite").write_text(directory.name, encoding="utf-8")

            config_status = migrator.ConfigStatus(path=codex_home / "config.toml", sqlite_home=config_home)
            with patch.dict(os.environ, {"CODEX_SQLITE_HOME": str(env_home)}):
                self.assertEqual(
                    migrator.resolve_state_db(codex_home, config_status, explicit_path=None),
                    config_home / "state_5.sqlite",
                )

            config_status.sqlite_home = None
            with patch.dict(os.environ, {"CODEX_SQLITE_HOME": str(env_home)}):
                self.assertEqual(
                    migrator.resolve_state_db(codex_home, config_status, explicit_path=None),
                    env_home / "state_5.sqlite",
                )

            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(
                    migrator.resolve_state_db(codex_home, config_status, explicit_path=None),
                    codex_home / "state_5.sqlite",
                )

    def test_inspect_config_reads_sqlite_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config_path = root / "config.toml"
            config_path.write_text('sqlite_home = "sqlite"\n', encoding="utf-8")

            status = migrator.inspect_config(config_path)

            self.assertEqual(status.sqlite_home, Path("sqlite"))

    def test_state_db_resolution_selects_highest_version_before_mtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            older_v5 = root / "state_5.sqlite"
            newer_v4 = root / "state_4.sqlite"
            ignored = root / "state_latest.sqlite"
            older_v5.write_text("v5", encoding="utf-8")
            newer_v4.write_text("v4", encoding="utf-8")
            ignored.write_text("ignored", encoding="utf-8")
            os.utime(older_v5, (100, 100))
            os.utime(newer_v4, (200, 200))

            self.assertEqual(sorted(migrator.iter_state_db_candidates(root), reverse=True), [(5, 100.0, older_v5), (4, 200.0, newer_v4)])
            self.assertEqual(
                migrator.resolve_state_db(
                    root,
                    migrator.ConfigStatus(path=root / "config.toml"),
                    explicit_path=None,
                ),
                older_v5,
            )


class BackupTests(unittest.TestCase):
    def test_rollout_backup_preserves_path_relative_to_codex_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            codex_home = root / "codex-home"
            backup_root = root / "backup"
            path = codex_home / "sessions" / "2026" / "rollout.jsonl"
            path.parent.mkdir(parents=True)
            original = f"{rollout_line('custom')}\n"
            path.write_text(original, encoding="utf-8")

            migrator.rewrite_rollout_file(
                path=path,
                codex_home=codex_home,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=backup_root,
                report=migrator.RolloutReport(),
            )

            self.assertEqual(
                (backup_root / "sessions" / "2026" / "rollout.jsonl").read_text(encoding="utf-8"),
                original,
            )

    def test_sqlite_migration_backup_includes_db_wal_and_shm(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            db_path = root / "state_5.sqlite"
            backup_root = root / "backup"
            create_threads_db(db_path, ["custom"])
            wal_bytes = b"wal-sidecar"
            shm_bytes = b"shm-sidecar"
            Path(str(db_path) + "-wal").write_bytes(wal_bytes)
            Path(str(db_path) + "-shm").write_bytes(shm_bytes)

            migrator.migrate_sqlite(
                db_path=db_path,
                target_provider="openai",
                keep_providers=KEEP_OPENAI,
                apply=True,
                backup_root=backup_root,
            )

            self.assertTrue((backup_root / "sqlite" / "state_5.sqlite").exists())
            self.assertTrue((backup_root / "sqlite" / "state_5.sqlite-wal").exists())
            self.assertTrue((backup_root / "sqlite" / "state_5.sqlite-shm").exists())


if __name__ == "__main__":
    unittest.main()
