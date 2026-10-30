import json
from pathlib import Path

from ale_verify import write


def result() -> dict:
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
        return {"score": float(matched), "diagnostic": diagnostic}
    except (FileNotFoundError, json.JSONDecodeError, AttributeError):
        return {"score": 0.0, "diagnostic": "resource proof is missing or invalid"}


proof = result()
write({"reward": proof["score"], "proof": proof})
