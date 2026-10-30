from ale_verify import write


def greeting_matches(path: str, expected: str) -> dict:
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


greeting = greeting_matches("/home/user/output/result.txt", "hello world")
write({"reward": greeting["score"], "greeting": greeting})
