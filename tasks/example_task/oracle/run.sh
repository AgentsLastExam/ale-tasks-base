#!/usr/bin/env bash
# The known-good solution. `ale validate` first requires untouched zero rewards, then
# runs this in place of the agent and requires the same rewards to equal 1.0.
set -euo pipefail

greeting="$(python3 -c 'import json,os; print(json.load(open(os.environ["ALE_PARAMS_JSON"]))["greeting"])')"
printf '%s %s' "$greeting" "$(cat /home/user/input/word.txt)" > /home/user/output/result.txt
