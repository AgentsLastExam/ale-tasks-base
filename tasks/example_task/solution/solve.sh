#!/usr/bin/env bash
# The Task's reference solution, its calibration case `solution`. `ale calibrate` first
# requires an untouched reward of zero, then runs this in place of the agent and requires
# a reward of 1.0.
set -euo pipefail

printf 'hello %s' "$(cat /home/user/input/word.txt)" > /home/user/output/result.txt
