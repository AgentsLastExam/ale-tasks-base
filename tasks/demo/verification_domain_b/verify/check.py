from ale_verify import Verification
from verification_example import approved_record

verification = Verification()
verification.check(
    "approved",
    approved_record("/home/user/output/report.json"),
)
verification.aggregate("overall")
verification.write()
