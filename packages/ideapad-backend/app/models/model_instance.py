import uuid
from app.models.model_definition import ModelDefinition
from app.types import ModelConfig, ModelErrorDetailEnum
from app.exceptions import (
    ModelInferenceError,
    ModelShutdownError,
    to_http_exception
)

class ModelInstance:
    """
    Represents a persistent model session tied to a conversation, identified by a UUID.
    Handles session lifecycle, including warm-up and resource cleanup.
    """
    def __init__(self, config: ModelConfig):
        self.conversation_id = str(uuid.uuid4())
        self.config = config
        self.model = ModelDefinition(config)
        self.run_warm_up()
        self.history: list[dict[str, str]] = []

    def get_response(self, prompt: str) -> str:
        try:
            # 1) append user turn
            self.history.append({"role": "user", "content": prompt})
            # 2) run inference via generate_response (which now uses chat API)
            answer = self.model.generate_response(prompt)
            # 3) append assistant turn
            self.history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            raise to_http_exception(ModelInferenceError(ModelErrorDetailEnum.MODEL_INFERENCE_ERROR)) from e

    def run_warm_up(self):
        """
        Warm up the model by performing a dummy inference.
        """
        try:
            self.model.generate_response(prompt="Warm up")
        except Exception as e:
            raise to_http_exception(ModelInferenceError(ModelErrorDetailEnum.MODEL_INFERENCE_ERROR)) from e

    def get_conversation_id(self) -> str:
        """
        Return the unique conversation ID associated with this model instance.
        """
        return self.conversation_id

    def shutdown(self):
        """
        Explicitly shut down the model resources.
        """
        try:
            self.model.close()
        except Exception as e:
            raise to_http_exception(ModelShutdownError(ModelErrorDetailEnum.MODEL_SHUTDOWN_ERROR)) from e
        
    def system_prompt(self) -> str:
        """
        Return the system prompt for the model.
        This can be used to set the context or initial state of the model.
        """
        return "You are a helpful coding assistant."
        
    def __enter__(self):
        """
        Support context manager usage for automatic resource management.
        """
        return self

    def __del__(self):
        """
        Automatically clean up resources upon object deletion.
        """
        try:
            self.shutdown()
        except Exception:
            pass  # Avoid throwing exceptions during object deletion