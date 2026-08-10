import json

from ale_verify import CheckResult, Verification


def approved_record(path: str) -> CheckResult:
    try:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, ValueError) as exc:
        return CheckResult(0.0, f"record could not be read: {exc}")
    return CheckResult(float(payload == {"approved": True}), "approval checked", payload)

verification = Verification()
verification.check(
    "approved",
    approved_record("/home/user/output/report.json"),
)
verification.aggregate("overall")
verification.write()
