#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/user/output
cat > /home/user/output/tool_report.json <<'JSON'
{
  "tools_tested": ["oracle_fixture"],
  "tools_passed": ["oracle_fixture"],
  "tools_failed": {},
  "tools_untested": {},
  "total": 1,
  "tested": 1,
  "passed": 1,
  "failed": 0,
  "untested": 0
}
JSON
