#!/usr/bin/env python3
"""
Clean Claude Code project prompt history from ~/.claude.json.

Older Claude Code versions stored per-project prompt history inside
~/.claude.json under projects[*].history. This script removes those history
arrays while preserving the rest of the configuration data.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def clean_claude_json() -> int:
    claude_json_path = Path.home() / ".claude.json"

    if not claude_json_path.exists():
        print("Error: ~/.claude.json not found")
        return 1

    original_size = claude_json_path.stat().st_size
    print(f"Original file size: {original_size / 1024 / 1024:.2f} MB")

    backup_path = claude_json_path.with_suffix(
        f".json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    print(f"Creating backup: {backup_path}")

    try:
        print("Reading file...")
        with open(claude_json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        with open(backup_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        history_count = 0
        history_size_total = 0

        if "projects" in data:
            for project_id in data["projects"]:
                project = data["projects"][project_id]
                if isinstance(project, dict) and "history" in project:
                    history_size = len(json.dumps(project["history"]))
                    history_size_total += history_size
                    history_count += 1

                    if history_size > 1024 * 1024:
                        print(
                            "Clearing large history for "
                            f"{project_id[:30]}... "
                            f"({history_size / 1024 / 1024:.2f} MB)"
                        )

                    project["history"] = []

        print(
            f"\nFound {history_count} project histories totaling "
            f"{history_size_total / 1024 / 1024:.2f} MB"
        )

        print("Writing cleaned file...")
        with open(claude_json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        new_size = claude_json_path.stat().st_size
        reduction_pct = ((original_size - new_size) / original_size) * 100

        print("\nSuccess!")
        print(f"   Original: {original_size / 1024 / 1024:.2f} MB")
        print(f"   New size: {new_size / 1024:.2f} KB")
        print(f"   Reduced by: {reduction_pct:.1f}%")
        print(f"\nBackup saved to: {backup_path}")
        print(f"   You can delete it with: rm {backup_path}")

        return 0

    except json.JSONDecodeError as error:
        print("Error: Invalid JSON in ~/.claude.json")
        print(f"   {error}")
        return 1
    except Exception as error:
        print(f"Error: {error}")
        if backup_path.exists() and not claude_json_path.exists():
            print("Restoring from backup...")
            backup_path.rename(claude_json_path)
        return 1


def main() -> int:
    print("Claude Code JSON Cleaner")
    print("=" * 40)

    claude_json_path = Path.home() / ".claude.json"
    if claude_json_path.exists():
        size_mb = claude_json_path.stat().st_size / 1024 / 1024
        if size_mb < 1:
            print(f"File is already small ({size_mb:.2f} MB), no cleaning needed!")
            response = input("Clean anyway? (y/N): ")
            if response.lower() != "y":
                return 0

    return clean_claude_json()


if __name__ == "__main__":
    sys.exit(main())
