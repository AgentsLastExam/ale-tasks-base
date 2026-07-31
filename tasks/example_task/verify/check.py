from ale_verify import Verification
from example_kit import greeting_matches

verification = Verification()
verification.check(
    "reward",
    greeting_matches("/home/user/output/result.txt"),
)
verification.write()
