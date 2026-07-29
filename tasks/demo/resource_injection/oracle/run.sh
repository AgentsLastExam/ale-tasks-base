#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import json
import secrets
from pathlib import Path

nonce = Path("/home/user/input/nonce.txt").read_text().strip()
fragment = secrets.token_hex(12).upper()
Path("/home/user/output/result.txt").write_text(
    f"SKILL-R7::{nonce}::{fragment}",
    encoding="utf-8",
)
Path("/home/user/output/mcp-call.json").write_text(
    json.dumps({"nonce": nonce, "fragment": fragment}, sort_keys=True),
    encoding="utf-8",
)
PY
