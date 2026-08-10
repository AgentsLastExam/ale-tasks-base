import json

from ale_verify import Verification, checks


verification = Verification()
expected = json.loads(open("assets/expected.json", encoding="utf-8").read())
verification.check(
    "public",
    checks.json_value("/home/user/output/result.json", "public", expected["public"]),
)
verification.check(
    "service",
    checks.json_value("/home/user/output/result.json", "service", expected["service"]),
)
verification.aggregate("overall")
verification.write()
