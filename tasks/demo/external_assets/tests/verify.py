import json

from ale_verify import checks, write


expected = json.loads(open("assets/expected.json", encoding="utf-8").read())
public = checks.json_value("/home/user/output/result.json", "public", expected["public"])
service = checks.json_value("/home/user/output/result.json", "service", expected["service"])
write(
    {
        "reward": (public["score"] + service["score"]) / 2,
        "public": public,
        "service": service,
    }
)
