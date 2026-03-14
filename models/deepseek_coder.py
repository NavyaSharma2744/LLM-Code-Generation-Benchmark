from transformers import pipeline
from models.model_interface import BaseModel


class DeepSeekCoderModel(BaseModel):
    def __init__(self, max_new_tokens: int = 128, temperature: float = 0.2, do_sample: bool = False):
        self.generator = pipeline(
            "text-generation",
            model="deepseek-ai/deepseek-coder-1.3b-base",
            device_map="auto",
        )
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.do_sample = do_sample

    def generate_code(self, prompt: str) -> str:
        output = self.generator(
            prompt,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            do_sample=self.do_sample,
            return_full_text=False,
        )
        return output[0]["generated_text"]
