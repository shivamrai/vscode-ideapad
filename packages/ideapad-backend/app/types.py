from typing import List, TypedDict
from enum import Enum

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """
    Configuration for a language model.

    Attributes:
        model_path (Path): Path to the .gguf model file.
        n_ctx (int): Maximum context size. Default is 2048.
        max_tokens (int): Max tokens to generate (aliased as 'model_tokens'). Default is 512.
        temperature (float): Sampling temperature. Default is 0.7.
        top_p (float): Nucleus sampling probability. Default is 0.95.
        top_k (int): Top-K sampling size. Default is 40.
        repeat_penalty (float): Penalty for repeated tokens. Default is 1.1.
        repeat_last_n (int): Window size for repeat penalty. Default is 64.
        num_threads (int): Number of CPU threads. Default is 4.
        num_predict (int): Batch size for predict calls. Default is 1.

    Config:
        allow_population_by_field_name (bool): Allows population of fields by their name.
    """

    model_path: str = Field("models/default.gguf", description="…")

    n_ctx: int = Field(2048, description="Maximum context size")
    max_tokens: int = Field(
        512, alias="model_tokens", description="Max tokens to generate"
    )
    temperature: float = Field(0.7, description="Sampling temperature")
    top_p: float = Field(0.95, description="Nucleus sampling probability")
    top_k: int = Field(40, description="Top-K sampling size")
    repeat_penalty: float = Field(1.1, description="Penalty for repeated tokens")
    repeat_last_n: int = Field(64, description="Window size for repeat penalty")
    num_threads: int = Field(4, description="Number of CPU threads")
    num_predict: int = Field(1, description="Batch size for predict calls")


class Config:
    allow_population_by_field_name = True


class ModelErrorDetailEnum(str, Enum):
    """
    A type for all detail exceptions in exception.py
    This is used to ensure that the error details are consistent across the application.
    """

    MODEL_LOAD_ERROR = "Failed to load the LLM model"
    MODEL_INFERENCE_ERROR = "Failed during model inference"
    MODEL_SHUTDOWN_ERROR = "Failed to shutdown the model properly"
    INVALID_PROMPT_ERROR = "Prompt must be a non-empty string"
    MODEL_INVALID_RESPONSE_ERROR = "Model returned invalid response structure."
    CONVERSATION_NOT_FOUND_ERROR = "Conversation not found"
    MODEL_INITIALIZATION_ERROR = "Model instance failed to initialize"


class ModelErrorDetail(TypedDict):
    detail: ModelErrorDetailEnum


class CompletionChoice(TypedDict):
    text: str
    index: int


class CompletionResult(TypedDict):
    choices: List[CompletionChoice]
