# Project Design

This project benchmarks multiple code generation LLMs on standard datasets.

## Pipeline
1. Load dataset
2. Build prompt
3. Generate code
4. Execute generated code with tests
5. Compute evaluation metrics
6. Save benchmark results

## Objective
To compare code generation models on correctness, execution success, and similarity to reference solutions.
