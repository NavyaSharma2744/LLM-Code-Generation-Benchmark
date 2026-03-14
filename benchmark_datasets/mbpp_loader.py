from typing import List, Dict
from datasets import load_dataset
from benchmark_datasets.dataset_loader import BaseDatasetLoader

class MBPPLoader(BaseDatasetLoader):
    def load(self, max_samples: int | None = None) -> List[Dict]:
        dataset = load_dataset("mbpp")["test"]

        samples = []
        for i, item in enumerate(dataset):
            if max_samples is not None and i >= max_samples:
                break

            test_cases = "\n".join(item.get("test_list", []))

            samples.append(
                {
                    "task_id": str(item["task_id"]),
                    "prompt": item["text"],
                    "test": test_cases,
                    "entry_point": "",
                    "reference_solution": item.get("code", ""),
                }
            )
        return samples
