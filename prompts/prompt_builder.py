def build_prompt(problem_text: str) -> str:
    return (
        "You are an expert Python programmer.\n"
        "Write only the Python function needed to solve the problem.\n"
        "Do not include explanations.\n\n"
        f"Problem:\n{problem_text}\n"
    )
