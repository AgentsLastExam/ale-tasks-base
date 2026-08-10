from ale_verify import Verification, checks

verification = Verification()
verification.check(
    "nested_container",
    checks.text_equals(
        "/home/user/output/nested-container.txt",
        "nested-container-ok\n",
    ),
)
verification.write()
