from fastapi import HTTPException, status
from app.types import ModelErrorDetailEnum


# Base exception for all custom model-related errors
class ModelError(Exception):
    """Base exception for model-related errors."""

    pass


class ModelLoadError(ModelError):
    """Raised when the model fails to load."""

    def __init__(
        self, detail: ModelErrorDetailEnum = ModelErrorDetailEnum.MODEL_INFERENCE_ERROR
    ):
        self.detail = detail
        super().__init__(self.detail)


class ModelShutdownError(ModelError):
    """Raised when shutting down or cleaning up the model fails."""

    def __init__(
        self, detail: ModelErrorDetailEnum = ModelErrorDetailEnum.MODEL_SHUTDOWN_ERROR
    ):
        self.detail = detail
        super().__init__(self.detail)


class InvalidPromptError(ModelError):
    """Raised when an empty or invalid prompt is provided."""

    def __init__(
        self, detail: ModelErrorDetailEnum = ModelErrorDetailEnum.INVALID_PROMPT_ERROR
    ):
        self.detail = detail
        super().__init__(self.detail)


class ModelInferenceError(ModelError):
    """Raised when inference on the model fails."""

    def __init__(
        self, detail: ModelErrorDetailEnum = ModelErrorDetailEnum.MODEL_INFERENCE_ERROR
    ):
        self.detail = detail
        super().__init__(self.detail)


class ModelInvalidResponseError(ModelError):
    """Raised when the model returns an invalid response structure."""

    def __init__(
        self,
        detail: ModelErrorDetailEnum = ModelErrorDetailEnum.MODEL_INVALID_RESPONSE_ERROR,
    ):
        self.detail = detail
        super().__init__(self.detail)


class ConversationNotFoundError(ModelError):
    """Raised when an unknown conversation ID is used."""

    def __init__(
        self,
        detail: ModelErrorDetailEnum = ModelErrorDetailEnum.CONVERSATION_NOT_FOUND_ERROR,
    ):
        super().__init__(detail)


class ModelInitError(ModelError):
    """Raised when the model fails to initialize."""

    def __init__(
        self,
        detail: ModelErrorDetailEnum = ModelErrorDetailEnum.MODEL_INITIALIZATION_ERROR,
    ):
        super().__init__(detail)


# Utility function to convert internal exceptions to HTTP exceptions
def to_http_exception(exc: ModelError) -> HTTPException:
    if isinstance(exc, ModelLoadError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.detail
        )
    if isinstance(exc, ModelInferenceError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.detail
        )
    if isinstance(exc, ModelShutdownError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.detail
        )
    if isinstance(exc, InvalidPromptError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.detail)
    if isinstance(exc, ModelInvalidResponseError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.detail
        )
    if isinstance(exc, ConversationNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ModelInitError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
    )
