#!/usr/bin/env bash
set -euo pipefail
mkdir -p /home/user/output
install -o user -g user -m 644 /dev/null /home/user/output/answer.txt
