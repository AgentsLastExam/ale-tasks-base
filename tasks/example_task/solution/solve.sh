#!/usr/bin/env bash
# The known-good solution. `ale validate` first requires an untouched reward of zero, then
# runs this in place of the agent and requires reward to equal 1.0.
set -euo pipefail

printf 'hello %s' "$(cat /home/user/input/word.txt)" > /home/user/output/result.txt
