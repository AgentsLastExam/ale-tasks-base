#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/user/input /home/user/output
rm -f /home/user/output/result.txt /home/user/output/mcp-call.json
python3 - <<'PY' > /home/user/input/nonce.txt
import secrets
print(secrets.token_hex(8).upper())
PY
