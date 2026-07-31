"""Worked example of a reusable Task-repository verification package."""

import json
import os

from ale_verify import CheckResult

__all__ = ["greeting_matches", "read_params"]


def read_params():
    path = os.environ.get("ALE_TASK_PARAMETERS_PATH", os.environ["ALE_PARAMS_JSON"])
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def greeting_matches(path, word="world"):
    expected = f"{read_params()['greeting']} {word}"
    try:
        with open(path, encoding="utf-8") as handle:
            actual = handle.read()
    except OSError as exc:
        return CheckResult(0.0, f"result could not be read: {exc}")
    return CheckResult(
        float(actual == expected),
        "greeting matched" if actual == expected else "greeting differed",
        actual,
    )
