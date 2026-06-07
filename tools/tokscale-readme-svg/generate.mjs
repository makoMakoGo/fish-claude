#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..", "..");
const outputPath = path.join(repoRoot, "assets", "tokscale.svg");
const profileName = detectProfileName(repoRoot);

const result = spawnSync("tokscale", ["--json"], {
  cwd: repoRoot,
  encoding: "utf8",
  maxBuffer: 20 * 1024 * 1024,
});

if (result.error) {
  throw result.error;
}

if (result.status !== 0) {
  process.stderr.write(result.stderr || "tokscale --json failed\n");
  process.exit(result.status ?? 1);
}

const summary = JSON.parse(result.stdout);
const entries = Array.isArray(summary.entries) ? summary.entries : [];
const totalReasoning = entries.reduce((sum, entry) => sum + asNumber(entry.reasoning), 0);

const totalTokens =
  asNumber(summary.totalInput) +
  asNumber(summary.totalOutput) +
  asNumber(summary.totalCacheRead) +
  asNumber(summary.totalCacheWrite) +
  totalReasoning;

const generatedAt = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "UTC",
}).format(new Date());

const svg = renderSvg({
  profileName,
  totalTokens,
  totalCost: asNumber(summary.totalCost),
  generatedAt,
});

mkdirSync(path.dirname(outputPath), { recursive: true });
writeFileSync(outputPath, svg);
process.stdout.write(`wrote ${path.relative(repoRoot, outputPath)}\n`);

function asNumber(value) {
  return Number.isFinite(Number(value)) ? Number(value) : 0;
}

function detectProfileName(cwd) {
  const remote = spawnSync("git", ["remote", "get-url", "origin"], {
    cwd,
    encoding: "utf8",
  });

  if (remote.error) {
    throw remote.error;
  }
  if (remote.status !== 0) {
    throw new Error(remote.stderr || "git remote get-url origin failed");
  }

  const value = remote.stdout.trim();
  const match = value.match(/[:/]([^/:\s]+)\/([^/\s]+?)(?:\.git)?$/);
  if (!match) {
    throw new Error(`Could not parse GitHub owner from origin remote: ${value}`);
  }

  return match[1];
}

function fullNumber(value) {
  return new Intl.NumberFormat("en-US").format(Math.round(value));
}

function currency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function renderSvg(data) {
  const W = 600;
  const H = 166;
  const PAD = 22;
  const TITLE_BAR = 38;

  const parts = [];
  const add = (line) => parts.push(line);

  add('<?xml version="1.0" encoding="UTF-8"?>');
  add(`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Local Tokscale stats for @${escapeXml(data.profileName)}">`);
  add(`  <defs><clipPath id="win"><rect width="${W}" height="${H}" rx="12"/></clipPath></defs>`);
  add(`  <rect width="${W}" height="${H}" rx="12" fill="#FFFFFF"/>`);
  add(`  <g clip-path="url(#win)"><rect width="${W}" height="${TITLE_BAR}" fill="#EBEDF0"/></g>`);
  add(`  <line x1="0" y1="${TITLE_BAR}" x2="${W}" y2="${TITLE_BAR}" stroke="#D0D7DE"/>`);
  add(`  <rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="11.5" fill="none" stroke="#D0D7DE"/>`);
  add(`  <circle cx="${PAD + 4}" cy="${TITLE_BAR / 2}" r="5.5" fill="#FF5F56"/>`);
  add(`  <circle cx="${PAD + 22}" cy="${TITLE_BAR / 2}" r="5.5" fill="#FFBD2E"/>`);
  add(`  <circle cx="${PAD + 40}" cy="${TITLE_BAR / 2}" r="5.5" fill="#27C93F"/>`);
  add(`  <text x="${PAD + 60}" y="${TITLE_BAR / 2 + 4}" fill="#656D76" font-size="12" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">tokscale - @${escapeXml(data.profileName)}</text>`);
  add(`  <text x="${PAD}" y="70" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace"><tspan fill="#0969DA" font-weight="700">$</tspan><tspan fill="#1F2328"> tokscale stats</tspan></text>`);
  add(`  <text x="${PAD}" y="100" fill="#656D76" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">tokens</text>`);
  add(`  <text x="${PAD + 92}" y="100" fill="#0969DA" font-size="13" font-weight="700" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">${escapeXml(fullNumber(data.totalTokens))}</text>`);
  add(`  <text x="${PAD}" y="124" fill="#656D76" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">cost</text>`);
  add(`  <text x="${PAD + 92}" y="124" fill="#1A7F37" font-size="13" font-weight="700" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">${escapeXml(currency(data.totalCost))}</text>`);
  add(`  <text x="${PAD}" y="${H - 16}" fill="#656D76" font-size="11" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">Generated ${escapeXml(data.generatedAt)} (UTC)</text>`);
  add(`  <text x="${W - PAD}" y="${H - 16}" fill="#656D76" font-size="10" text-anchor="end" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">history cleaned; actual usage higher</text>`);
  add(`</svg>`);

  return parts.join("\n");
}
