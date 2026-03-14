from execution.sandbox import safe_exec


def run_generated_code(generated_code: str, test_code: str) -> dict:
    combined_code = f"{generated_code}\n\n{test_code}"
    success, error = safe_exec(combined_code)

    return {
        "compiled": success,
        "passed": success,
        "error": error,
    }
