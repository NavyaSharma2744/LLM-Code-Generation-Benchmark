# LLM Code Generation Benchmark

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Project](https://img.shields.io/badge/Type-Research%20Project-orange)
![Focus](https://img.shields.io/badge/Focus-Code%20Generation%20LLMs-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Stars](https://img.shields.io/github/stars/NavyaSharma2744/llm-code-generation-benchmark?style=social)

Benchmarking large language models for **code generation and program synthesis** using standard benchmarks such as HumanEval and MBPP.  
The project evaluates model performance using metrics like **Pass@k, compilation success rate, and CodeBLEU**.

---

## Environment

| Component | Version |
|----------|--------|
| Python | **3.14** |
| PyTorch | 2.x |
| Transformers | Latest |
| OS | Linux / macOS |

---

## Supported Models

This project benchmarks modern code generation models including:

- Code Llama
- StarCoder2
- DeepSeek Coder

---

## Benchmarks

- HumanEval
- MBPP

---

## Evaluation Metrics

- Pass@k
- Compilation Success Rate
- CodeBLEU

## Setup and Run (macOS / Linux)

# Clone the repository
git clone https://github.com/YOUR_USERNAME/llm-code-generation-benchmark.git
cd llm-code-generation-benchmark

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure Python treats folders as packages
touch benchmark_datasets/__init__.py
touch models/__init__.py
touch prompts/__init__.py
touch execution/__init__.py
touch evaluation/__init__.py
touch experiments/__init__.py

# Run the benchmark pipeline
python main.py

## Outputs

The benchmark pipeline generates the following files in the `results/` directory:

- `benchmark_results.csv` — aggregate evaluation metrics across all selected models
- `humaneval_results.csv` or `mbpp_results.csv` — dataset-specific benchmark summary
- `predictions.json` — per-sample generated code and execution outcomes
- `experiment_log.json` — metadata for the benchmark run including dataset, models, and generation settings