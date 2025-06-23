from llama_cpp import Llama
from app.types import ModelConfig

class ModelDefinition:
    """
    Loads and wraps the llama.cpp model into appmodel, handles inference, and manages resources.
    """

    def __init__(self, config: ModelConfig):
        self.model_path: str = config.get("model_path", "models/default.gguf")
        self.n_ctx: int = config.get("n_ctx", 2048)
        self.max_tokens: int = config.get("model_tokens", 512)
        self.temperature: float = config.get("temperature", 0.7)

        try:
            self.model: Llama = Llama(model_path=self.model_path, n_ctx=self.n_ctx)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama model: {e}") from e

    def generate_response(self, prompt: str) -> str:
        if not prompt:
            raise ValueError("Prompt must be a non-empty string")

        try:
            result = self.model.create_completion(
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stop=["\n"],
                stream=False
            )
        except Exception as e:
            raise RuntimeError(f"Model inference error: {e}") from e

        if isinstance(result, dict):  # Explicitly tell type checker we're handling non-stream response
            choices = result.get("choices", [])
            if choices and "text" in choices[0]:
                text = choices[0]["text"]
                return text.strip()

        raise RuntimeError("Model returned invalid response structure.")

    def close(self):
        """
        Safely closes the llama model and releases resources.
        """
        if hasattr(self.model, "close"):
            try:
                self.model.close()
            except Exception as e:
                raise RuntimeError(f"Error during model cleanup: {e}") from e