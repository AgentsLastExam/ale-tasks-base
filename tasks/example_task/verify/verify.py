import json
import os

from ale_verify import write


def greeting_matches(path: str, word: str = "world") -> dict:
    params_path = os.environ.get("ALE_TASK_PARAMETERS_PATH", os.environ["ALE_PARAMS_JSON"])
    with open(params_path, encoding="utf-8") as handle:
        expected = f"{json.load(handle)['greeting']} {word}"
    try:
        with open(path, encoding="utf-8") as handle:
            actual = handle.read()
    except OSError as exc:
        return {"score": 0.0, "diagnostic": f"result could not be read: {exc}"}
    return {
        "score": float(actual == expected),
        "diagnostic": "greeting matched",
        "raw_value": actual,
    }


reward = greeting_matches("/home/user/output/result.txt")
write({"overall": reward["score"], "reward": reward})
