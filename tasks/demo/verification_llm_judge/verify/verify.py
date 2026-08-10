from ale_verify import Verification

verification = Verification()
verification.judge(
    "llm",
    "correctness",
    prompt=(
        "Judge whether answer.txt correctly explains that shorter blue wavelengths "
        "are scattered more strongly by Earth's atmosphere. An empty answer is no."
    ),
    rubric={
        "no": {
            "score": 0.0,
            "description": "The answer is empty or materially incorrect.",
        },
        "yes": {
            "score": 1.0,
            "description": "The answer correctly explains wavelength-dependent scattering.",
        },
    },
    files=["/home/user/output/answer.txt"],
)
verification.aggregate("overall")
verification.write()
