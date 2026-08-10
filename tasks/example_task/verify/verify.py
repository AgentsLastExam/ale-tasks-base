import json
import os

from ale_verify import CheckResult, Verification


def greeting_matches(path: str, word: str = "world") -> CheckResult:
    params_path = os.environ.get("ALE_TASK_PARAMETERS_PATH", os.environ["ALE_PARAMS_JSON"])
    with open(params_path, encoding="utf-8") as handle:
        expected = f"{json.load(handle)['greeting']} {word}"
    try:
        with open(path, encoding="utf-8") as handle:
            actual = handle.read()
    except OSError as exc:
        return CheckResult(0.0, f"result could not be read: {exc}")
    return CheckResult(float(actual == expected), "greeting matched", actual)

verification = Verification()
verification.check(
    "reward",
    greeting_matches("/home/user/output/result.txt"),
)
verification.write()
