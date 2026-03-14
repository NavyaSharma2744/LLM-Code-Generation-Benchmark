import json
import os
from datetime import datetime

import pandas as pd
import yaml
from tqdm import tqdm

from benchmark_datasets.humaneval_loader import HumanEvalLoader
from benchmark_datasets.mbpp_loader import MBPPLoader
from evaluation.codebleu import compute_codebleu
from evaluation.compile_rate import compute_compile_rate
from evaluation.passk import compute_pass_at_k
from execution.code_runner import run_generated_code
from models.codellama import CodeLlamaModel
from models.deepseek_coder import DeepSeekCoderModel
from models.starcoder2 import StarCoder2Model
from prompts.prompt_builder import build_prompt


def get_dataset_loader(name: str):
    if name == "humaneval":
        return HumanEvalLoader()
    if name == "mbpp":
        return MBPPLoader()
    raise ValueError(f"Unsupported dataset: {name}")


def get_model(name: str, generation_cfg: dict):
    if name == "codellama":
        return CodeLlamaModel(**generation_cfg)
    if name == "starcoder2":
        return StarCoder2Model(**generation_cfg)
    if name == "deepseek_coder":
        return DeepSeekCoderModel(**generation_cfg)
    raise ValueError(f"Unsupported model: {name}")


def run_experiment(config_path: str = "configs/benchmark.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    os.makedirs("results", exist_ok=True)

    dataset_name = config["dataset"]
    dataset_loader = get_dataset_loader(dataset_name)
    samples = dataset_loader.load(max_samples=config["max_samples"])

    all_rows = []
    detailed_predictions = []

    for model_name in config["models"]:
        print(f"\nRunning model: {model_name}")
        model = get_model(model_name, config["generation"])

        model_results = []
        predictions = []
        references = []

        for sample in tqdm(samples, desc=f"{model_name} on {dataset_name}"):
            prompt = build_prompt(sample["prompt"])
            generated_code = model.generate_code(prompt)
            execution_result = run_generated_code(generated_code, sample["test"])

            predictions.append(generated_code)
            references.append(sample["reference_solution"])
            model_results.append(execution_result)

            detailed_predictions.append(
                {
                    "model": model_name,
                    "dataset": dataset_name,
                    "task_id": sample["task_id"],
                    "prompt": sample["prompt"],
                    "generated_code": generated_code,
                    "reference_solution": sample["reference_solution"],
                    "compiled": execution_result["compiled"],
                    "passed": execution_result["passed"],
                    "error": execution_result["error"],
                }
            )

        compile_rate = compute_compile_rate(model_results)
        pass_at_1 = compute_pass_at_k(model_results, k=1)
        codebleu = compute_codebleu(predictions, references)

        all_rows.append(
            {
                "model": model_name,
                "dataset": dataset_name,
                "compile_rate": compile_rate,
                "pass@1": pass_at_1,
                "codebleu": codebleu,
            }
        )

    df = pd.DataFrame(all_rows)

    # Main aggregate result file
    output_file = config.get("output_file", "results/benchmark_results.csv")
    df.to_csv(output_file, index=False)

    # Dataset-specific result file
    dataset_output_file = f"results/{dataset_name}_results.csv"
    df.to_csv(dataset_output_file, index=False)

    # Detailed predictions
    with open("results/predictions.json", "w", encoding="utf-8") as f:
        json.dump(detailed_predictions, f, indent=2, ensure_ascii=False)

    # Experiment log
    experiment_log = {
        "timestamp": datetime.now().isoformat(),
        "dataset": dataset_name,
        "max_samples": config["max_samples"],
        "models": config["models"],
        "generation": config["generation"],
        "num_tasks_loaded": len(samples),
        "aggregate_results_file": output_file,
        "dataset_results_file": dataset_output_file,
        "predictions_file": "results/predictions.json",
    }

    with open("results/experiment_log.json", "w", encoding="utf-8") as f:
        json.dump(experiment_log, f, indent=2, ensure_ascii=False)

    print("\nBenchmark completed.")
    print(df)
    print(f"\nSaved aggregate results to: {output_file}")
    print(f"Saved dataset-specific results to: {dataset_output_file}")
    print("Saved detailed predictions to: results/predictions.json")
    print("Saved experiment log to: results/experiment_log.json")
