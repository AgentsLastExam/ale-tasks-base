from ale_verify import checks, write

format_check = checks.json_value(
    "/home/user/output/result.json",
    "status",
    "ok",
)
value_check = checks.json_value(
    "/home/user/output/result.json",
    "value",
    7,
)
write(
    {
        "overall": (format_check["score"] + value_check["score"]) / 2,
        "format": format_check,
        "value": value_check,
        "measurements": {"checked_files": 1},
    }
)
