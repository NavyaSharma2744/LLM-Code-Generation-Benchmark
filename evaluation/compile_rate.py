def compute_compile_rate(results: list[dict]) -> float:
    if not results:
        return 0.0
    compiled_count = sum(1 for r in results if r["compiled"])
    return compiled_count / len(results)
