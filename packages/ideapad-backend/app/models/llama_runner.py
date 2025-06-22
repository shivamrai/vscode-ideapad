# We need to write a POST /chat handler and wire it to a stub model class in llama_runner.py.
#this is a class that will handle the llama model inference

from fastapi import HTTPException
from llama_cpp import Llama
from typing import TypedDict

class ModelConfig(TypedDict):
    model_path: str
    n_ctx: int
    model_tokens: int
    temperature: float


class LlamaModel:
    def __init__(self, config: ModelConfig):
        self.model_path = config.get("model_path", "models/default.gguf")
        self.n_ctx = config.get("n_ctx", 2048)
        self.max_tokens = config.get("model_tokens", 512)
        self.temperature = config.get("temperature", 0.7)

        try:
            self.model = Llama(model_path=self.model_path, n_ctx=self.n_ctx)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model initialization error: {str(e)}")

    def generate_response(self, prompt: str) -> str:
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt must be a non-empty string")

        result = self.model.create_completion(
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stop=["\n"]
            )

        text = ""
        if (
            isinstance(result, dict)
            and "choices" in result
            and len(result["choices"]) > 0
            and "text" in result["choices"][0]
            ):
            text = result["choices"][0]["text"]
        return text.strip()


class LlamaRunner:
    def __init__(self, config: ModelConfig):
        self.config = config
        # Initialize the model here (e.g., load the model from the path)
        # self.model = load_model(model_path)

    def run_inference(self, prompt: str) -> str:
        # This method should run inference on the model and return the response
        # For now, we will return a dummy response
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt must be a non-empty string")
        return self.get_response(prompt, self.config)
    
    def get_response(self, prompt: str, config: ModelConfig) -> str:
        """
        Get a response from the model based on the provided prompt.
        """
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt must be a non-empty string")
        try:
            response = LlamaModel(config).generate_response(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")
        return response