#!/usr/bin/env bash
set -euo pipefail

python3 -m http.server 8765 \
  --bind 127.0.0.1 \
  --directory assets \
  >/tmp/ale-external-assets-http.log 2>&1 &

python3 - <<'PY'
import time
from urllib.request import urlopen

for _ in range(50):
    try:
        with urlopen("http://127.0.0.1:8765/service-response.txt", timeout=1) as response:
            if response.read().decode().strip() == "dynamic-value":
                break
    except OSError:
        time.sleep(0.1)
else:
    raise SystemExit("setup service did not become ready")
PY
