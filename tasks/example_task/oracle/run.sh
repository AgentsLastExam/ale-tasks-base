#!/usr/bin/env bash
# The known-good solution. `ale validate` runs this in place of the agent and requires
# every verifier reward to equal 1.0; a task nobody can solve never reaches the registry.
set -euo pipefail

greeting="$(python3 -c 'import json,os; print(json.load(open(os.environ["ALE_PARAMS_JSON"]))["greeting"])')"
printf '%s %s' "$greeting" "$(cat /home/user/input/word.txt)" > /home/user/output/result.txt
