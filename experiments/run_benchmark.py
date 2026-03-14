import yaml
import pandas as pd
from tqdm import tqdm

from datasets.humaneval_loader import HumanEvalLoader
from datasets.mbpp_loader import MBPPLoader
from prompts.prompt_builder import build_prompt
from execution.code_runner import run_generated_code
from evaluation.compile_rate import compute_compile_rate
from evaluation.passk import compute_pass_at_k
from evaluation.codebleu import compute_codebleu

from models.codellama import CodeLlamaModel
from models.starcoder2 import StarCoder2Model
from models.deepseek_coder import DeepSeekCoderModel


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

    dataset_loader = get_dataset_loader(config["dataset"])
    samples = dataset_loader.load(max_samples=config["max_samples"])

    all_rows = []

    for model_name in config["models"]:
        print(f"\nRunning model: {model_name}")
        model = get_model(model_name, config["generation"])

        model_results = []
        predictions = []
        references = []

        for sample in tqdm(samples):
            prompt = build_prompt(sample["prompt"])
            generated_code = model.generate_code(prompt)
            execution_result = run_generated_code(generated_code, sample["test"])

            predictions.append(generated_code)
            references.append(sample["reference_solution"])
            model_results.append(execution_result)

        compile_rate = compute_compile_rate(model_results)
        pass_at_1 = compute_pass_at_k(model_results, k=1)
        codebleu = compute_codebleu(predictions, references)

        all_rows.append(
            {
                "model": model_name,
                "dataset": config["dataset"],
                "compile_rate": compile_rate,
                "pass@1": pass_at_1,
                "codebleu": codebleu,
            }
        )

    df = pd.DataFrame(all_rows)
    df.to_csv(config["output_file"], index=False)
    print("\nBenchmark completed.")
    print(df)
