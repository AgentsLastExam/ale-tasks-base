from ale_verify import judge, write

RUBRIC = {
    "no": {
        "score": 0.0,
        "description": "The executable is missing, fails, or prints another value.",
    },
    "yes": {
        "score": 1.0,
        "description": "The executable runs successfully and prints exactly hello.",
    },
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "choice": {"enum": list(RUBRIC)},
        "reasoning": {"type": "string", "minLength": 1},
    },
    "required": ["choice", "reasoning"],
    "additionalProperties": False,
}

assessment = judge(
    "agent",
    "functional",
    prompt=(
        "Inspect /home/user/output/hello.sh. Execute it if present and judge whether "
        "it is executable and prints exactly hello.\n\n"
        'Set "choice" to exactly one rubric label and explain it in "reasoning".\n'
        + "\n".join(f"- {label}: {choice['description']}" for label, choice in RUBRIC.items())
    ),
    output_schema=OUTPUT_SCHEMA,
)
functional = {"score": RUBRIC[assessment["choice"]]["score"], **assessment}
write({"reward": functional["score"], "functional": functional})
