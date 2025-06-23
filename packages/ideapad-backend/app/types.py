from typing import List, TypedDict
from enum import Enum


class ModelConfig(TypedDict):
    model_path: str
    n_ctx: int
    model_tokens: int
    temperature: float


class ModelErrorDetailEnum(str, Enum):
    MODEL_LOAD_ERROR = "Failed to load the LLM model"
    MODEL_INFERENCE_ERROR = "Failed during model inference"
    MODEL_SHUTDOWN_ERROR = "Failed to shutdown the model properly"
    INVALID_PROMPT_ERROR = "Prompt must be a non-empty string"
    MODEL_INVALID_RESPONSE_ERROR = "Model returned invalid response structure."
    CONVERSATION_NOT_FOUND_ERROR = "Conversation not found"
    MODEL_INITIALIZATION_ERROR = "Model instance failed to initialize"

# generate a type for all detail exceptions in exception.py
class ModelErrorDetail(TypedDict):
    detail: ModelErrorDetailEnum

class CompletionChoice(TypedDict):
    text: str
    index: int

class CompletionResult(TypedDict):
    choices: List[CompletionChoice]