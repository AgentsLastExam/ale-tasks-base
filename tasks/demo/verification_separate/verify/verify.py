from ale_verify import checks, write

result = checks.json_value("/home/user/output/result.json", "status", "ok")
report = checks.text_equals("/var/lib/ale-report/state.txt", "ready")
write(
    {
        "overall": (result["score"] + report["score"]) / 2,
        "result": result,
        "report": report,
    }
)
