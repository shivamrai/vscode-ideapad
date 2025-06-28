from pathlib import Path
from llama_cpp import Llama
from app.types import ModelConfig


class ModelDefinition:
    """
    Loads and wraps the llama.cpp model into appmodel, handles inference, and manages resources.
    """

    def __init__(self, config: ModelConfig):
        self.n_ctx: int = getattr(config, "n_ctx", 2048)
        self.max_tokens: int = getattr(config, "model_tokens", 512)
        self.temperature: float = getattr(config, "temperature", 0.7)
        self.top_p: float = getattr(config, "top_p", 0.95)
        self.top_k: int = getattr(config, "top_k", 40)
        self.repeat_penalty: float = getattr(config, "repeat_penalty", 1.1)
        self.repeat_last_n: int = getattr(config, "repeat_last_n", 64)
        self.num_threads: int = getattr(config, "num_threads", 4)
        self.num_predict: int = getattr(config, "num_predict", 1)

        raw_path = getattr(config, "model_path", "models/default.gguf")
        candidate = Path(raw_path)
        # Resolve relative paths against project root
        if not candidate.is_absolute():
            project_root = Path(__file__).resolve().parents[4]
            candidate = (project_root / raw_path).expanduser()
        else:
            candidate = candidate.expanduser()
        if not candidate.exists():
            raise RuntimeError(f"Model path does not exist: {candidate}")
        self.model_path = str(candidate)

        try:
            self.model: Llama = Llama(model_path=self.model_path, n_ctx=self.n_ctx)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama model: {e}") from e

    def generate_response(self, prompt: str) -> str:
        if not prompt:
            raise ValueError("Prompt must be a non-empty string")

        try:
            result = self.model.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stop=["\n"],
                stream=False,
            )
        except Exception as e:
            raise RuntimeError(f"Model inference error: {e}") from e

        if isinstance(
            result, dict
        ):  # Explicitly tell type checker we're handling non-stream response
            choices = result.get("choices", [])
            if (
                choices
                and "message" in choices[0]
                and "content" in choices[0]["message"]
            ):
                text = choices[0]["message"]["content"]
                if text is not None:
                    return text.strip()
                else:
                    return ""

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
