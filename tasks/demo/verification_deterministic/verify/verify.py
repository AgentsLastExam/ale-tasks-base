from ale_verify import Verification, checks

verification = Verification()
verification.check(
    "format",
    checks.json_value(
        "/home/user/output/result.json",
        "status",
        "ok",
    ),
)
verification.check(
    "value",
    checks.json_value(
        "/home/user/output/result.json",
        "value",
        7,
    ),
)
verification.stat("checked_files", 1)
verification.aggregate("overall")
verification.write()
