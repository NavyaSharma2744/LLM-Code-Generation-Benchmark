def compute_pass_at_k(results: list[dict], k: int = 1) -> float:
    """
    Simplified Pass@k for one generation per problem.
    In this starter version, Pass@1 = accuracy.
    """
    if not results:
        return 0.0
    passed_count = sum(1 for r in results if r["passed"])
    return passed_count / len(results)
