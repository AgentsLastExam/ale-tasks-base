#!/usr/bin/env bash
set -euo pipefail
mkdir -p /home/user/output
printf '{"status":"ok","value":7}\n' > /home/user/output/result.json
