#!/usr/bin/env bash
set -euo pipefail
printf '{"status":"ok"}\n' > /home/user/output/result.json
printf 'ready' > /var/lib/ale-report/state.txt
