from abc import ABC, abstractmethod
from typing import List, Dict


class BaseDatasetLoader(ABC):
    @abstractmethod
    def load(self, max_samples: int | None = None) -> List[Dict]:
        """Load dataset samples in a common format."""
        raise NotImplementedError
