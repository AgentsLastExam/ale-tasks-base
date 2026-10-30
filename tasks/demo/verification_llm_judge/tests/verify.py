from pathlib import Path

from ale_verify import EvidenceError, judge, write

ANSWER = Path("/home/user/output/answer.txt")
RUBRIC = {
    "no": {
        "score": 0.0,
        "description": "The answer is empty or materially incorrect.",
    },
    "yes": {
        "score": 1.0,
        "description": "The answer correctly explains wavelength-dependent scattering.",
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


def correctness() -> dict:
    # A missing or unusable answer is the solver's outcome: it scores zero, with no model call.
    if ANSWER.is_symlink() or not ANSWER.is_file():
        return {"score": 0.0, "diagnostic": "answer.txt is missing or not a regular file"}
    try:
        assessment = judge(
            "llm",
            "correctness",
            prompt=(
                "Judge whether answer.txt correctly explains that shorter blue wavelengths "
                "are scattered more strongly by Earth's atmosphere. An empty answer is no.\n\n"
                'Set "choice" to exactly one rubric label and explain it in "reasoning".\n'
                + "\n".join(
                    f"- {label}: {choice['description']}" for label, choice in RUBRIC.items()
                )
            ),
            files=[str(ANSWER)],
            output_schema=OUTPUT_SCHEMA,
        )
    except EvidenceError as exc:
        return {"score": 0.0, "diagnostic": f"answer.txt is unusable as evidence: {exc}"}
    return {"score": RUBRIC[assessment["choice"]]["score"], **assessment}


result = correctness()
write({"reward": result["score"], "correctness": result})
