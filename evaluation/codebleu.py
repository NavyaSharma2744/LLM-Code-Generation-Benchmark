def compute_codebleu(predictions: list[str], references: list[str]) -> float:
    """
    Placeholder implementation.
    Replace with real CodeBLEU package or custom implementation later.
    """
    if not predictions or not references:
        return 0.0

    exact_matches = sum(1 for p, r in zip(predictions, references) if p.strip() == r.strip())
    return exact_matches / len(predictions)
