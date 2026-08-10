from ale_verify import Verification, checks

verification = Verification()
verification.check(
    "result",
    checks.json_value("/home/user/output/result.json", "status", "ok"),
)
verification.check(
    "report",
    checks.text_equals("/var/lib/ale-report/state.txt", "ready"),
)
verification.aggregate("overall")
verification.write()
