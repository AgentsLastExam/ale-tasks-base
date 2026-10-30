import json

from ale_verify import write


def approved_record(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, ValueError) as exc:
        return {"score": 0.0, "diagnostic": f"record could not be read: {exc}"}
    return {
        "score": float(payload == {"approved": True}),
        "diagnostic": "approval checked",
        "raw_value": payload,
    }


approved = approved_record("/home/user/output/report.json")
write({"reward": approved["score"], "approved": approved})
