"""Example reusable domain verification criterion."""

import json

from ale_verify import CheckResult

__all__ = ["approved_record"]


def approved_record(path):
    try:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, ValueError) as exc:
        return CheckResult(0.0, f"record could not be read: {exc}")
    approved = payload == {"approved": True}
    return CheckResult(
        float(approved),
        "record is approved" if approved else "record is not approved",
        payload,
    )
