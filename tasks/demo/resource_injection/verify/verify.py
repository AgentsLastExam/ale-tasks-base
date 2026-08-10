import json
from pathlib import Path

from ale_verify import CheckResult, Verification


def result() -> CheckResult:
    try:
        nonce = Path("/home/user/input/nonce.txt").read_text().strip()
        actual = Path("/home/user/output/result.txt").read_text().strip()
        receipt = json.loads(Path("/home/user/output/mcp-call.json").read_text())
        fragment = receipt.get("fragment")
        matched = (
            isinstance(fragment, str)
            and len(fragment) == 24
            and receipt.get("nonce") == nonce
            and actual == f"SKILL-R7::{nonce}::{fragment}"
        )
        diagnostic = "resource proof matched" if matched else "resource proof differed"
        return CheckResult(float(matched), diagnostic)
    except (FileNotFoundError, json.JSONDecodeError, AttributeError):
        return CheckResult(0.0, "resource proof is missing or invalid")


verification = Verification()
verification.check("reward", result())
verification.write()
