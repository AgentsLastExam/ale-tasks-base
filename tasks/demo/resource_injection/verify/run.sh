#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import json
import os
from pathlib import Path

nonce = Path("/home/user/input/nonce.txt").read_text().strip()
actual = Path("/home/user/output/result.txt").read_text().strip()
receipt = json.loads(Path("/home/user/output/mcp-call.json").read_text())
expected = f"SKILL-R7::{nonce}::{receipt.get('fragment', '')}"
reward = float(
    actual == expected
    and receipt.get("nonce") == nonce
    and isinstance(receipt.get("fragment"), str)
    and len(receipt["fragment"]) == 24
)
Path(os.environ["ALE_VERDICT_PATH"]).write_text(
    json.dumps({"rewards": {"reward": reward}})
)
PY
