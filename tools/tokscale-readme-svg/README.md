# tokscale-readme-svg

Generate the repository-local Tokscale README card.

Run from the repo root:

```bash
node tools/tokscale-readme-svg/generate.mjs
```

The script reads local `tokscale --json` data and writes [`assets/tokscale.svg`](../../assets/tokscale.svg).
