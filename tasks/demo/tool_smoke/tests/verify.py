"""Score the agent's own tool report: passed tools over every tool it identified.

Nothing in the sandbox can observe which tool produced an effect, so the report is the
agent's account; live acceptance audits the trajectory for the calls behind it. The
arithmetic is not trusted: wherever the lists are present, the counts come from them.
"""

import json
from pathlib import Path

from ale_verify import write

REPORT = Path("/home/user/output/tool_report.json")


def count(report: dict, field: str, listing: str) -> int:
    value = report.get(listing)
    if isinstance(value, (list, dict)) and value:
        return len(value)
    number = report.get(field)
    return number if isinstance(number, int) and number > 0 else 0


def result() -> dict:
    try:
        report = json.loads(REPORT.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {"reward": 0.0, "reason": "no readable tool_report.json"}
    if not isinstance(report, dict):
        return {"reward": 0.0, "reason": "the report is not an object"}

    tested = count(report, "tested", "tools_tested")
    passed = count(report, "passed", "tools_passed")
    failed = count(report, "failed", "tools_failed")
    untested = count(report, "untested", "tools_untested")
    claimed = report.get("total")
    # A total smaller than what was reported would score above 1.
    total = max(claimed if isinstance(claimed, int) else 0, tested + untested)
    if total == 0:
        return {"reward": 0.0, "reason": "no tools identified"}
    # An agent cannot pass more tools than it called.
    passed = min(passed, tested)
    return {
        "reward": passed / total,
        "total": total,
        "tested": tested,
        "passed": passed,
        "failed": failed,
        "untested": untested,
    }


write(result())
