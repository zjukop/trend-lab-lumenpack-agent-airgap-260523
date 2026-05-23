# LumenPack: Air-Gapped AI Agent Context Transfer

Minimal Python starter for packaging small AI-agent context bundles into checksummed chunks that can later be rendered as optical frames by a static web demo.

## Quick start

```bash
python -m pip install -e .[dev]
lumenpack "hello airgap"
python -m lumenpack_agent_airgap.main --text "repo context" --chunk-size 8
pytest
```

## What is included

- Tiny CLI for chunking text into resumable, checksummed JSON frames
- Smoke test
- Python 3.11+ packaging via `pyproject.toml`

## Next steps

- Add static `index.html` transmitter/receiver demo
- Add QR/flicker optical encoding
- Add agent presets for Claude Code, Gemini CLI, Kimi Code, and repo bundles
