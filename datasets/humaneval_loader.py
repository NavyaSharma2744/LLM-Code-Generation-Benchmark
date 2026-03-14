from typing import List, Dict
from datasets import load_dataset
from datasets.dataset_loader import BaseDatasetLoader


class HumanEvalLoader(BaseDatasetLoader):
    def load(self, max_samples: int | None = None) -> List[Dict]:
        dataset = load_dataset("openai_humaneval")["test"]

        samples = []
        for i, item in enumerate(dataset):
            if max_samples is not None and i >= max_samples:
                break

            samples.append(
                {
                    "task_id": item["task_id"],
                    "prompt": item["prompt"],
                    "test": item["test"],
                    "entry_point": item["entry_point"],
                    "reference_solution": item.get("canonical_solution", ""),
                }
            )
        return samples
