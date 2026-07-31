from ale_verify import Verification

verification = Verification()
verification.judge(
    "agent",
    "functional",
    prompt=(
        "Inspect /home/user/output/hello.sh. Execute it if present and judge whether "
        "it is executable and prints exactly hello."
    ),
    rubric={
        "no": {
            "score": 0.0,
            "description": "The executable is missing, fails, or prints another value.",
        },
        "yes": {
            "score": 1.0,
            "description": "The executable runs successfully and prints exactly hello.",
        },
    },
)
verification.aggregate("overall")
verification.write()
