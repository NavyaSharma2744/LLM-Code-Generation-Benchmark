from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def generate_code(self, prompt: str) -> str:
        """Generate code from a prompt."""
        raise NotImplementedError
