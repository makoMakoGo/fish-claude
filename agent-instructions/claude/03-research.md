# Research (No Guessing)

If something is unfamiliar or version-sensitive, look it up — never guess.

## Library Docs

<important if="you need current docs for a library, framework, SDK, API, CLI tool, or cloud service">
- Use `Context7` (`resolve-library-id` → `query-docs`).
</important>

## General Web Search Priority

<important if="you need general web search or non-library information">
- Prefer the `grok-search` skill for general / non-library queries.
- If `grok-search` is unavailable or not usable, use any available search MCP among `brave-search`, `exa-search`, or `serper-search`.
- Use the built-in `Web Search` tool only as the final fallback.
</important>

## Version and Source Checks

<important if="behaviour may differ across versions">
- First identify the project's version (lockfile/config), then query docs for that version.
- Source priority: official docs > changelog > upstream repo > community posts.
</important>
