from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

from app.models.model_runner import ModelRunner
from app.schemas import (
    StartConversationResponse,
    ContinueConversationRequest,
    ContinueConversationResponse,
    EndConversationRequest,
    EndConversationResponse,
    ChangeModelRequest,
)
from app.exceptions import ModelLoadError, to_http_exception
from app.types import ModelErrorDetailEnum
from app.api.session_manager import add_runner, get_runner_or_404, pop_runner_or_404

# Load config
CONFIG_PATH = Path(__file__).resolve().parents[2] / "model_config.json"
with open(CONFIG_PATH) as f:
    config = json.load(f)

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/model_info")
async def model_info() -> dict[str, str]:
    """
    Get information about the model.
    Returns the model path and other relevant details.
    """
    return {
        "model_path": str(config["model_path"]),
        "description": "Llama model for inference",
        "version": "1.0.0"
    }

@router.post("/start_conversation", response_model=StartConversationResponse)
async def start_conversation():
    """
    Initialize a new model session and return its conversation ID.
    """
    runner = ModelRunner(config)
    runner.start_model()
    if not hasattr(runner, "model_instance") or runner.model_instance is None:
        raise to_http_exception(ModelLoadError(detail=ModelErrorDetailEnum.MODEL_INITIALIZATION_ERROR))
    cid = runner.model_instance.get_conversation_id()
    add_runner(cid, runner)
    return {"conversation_id": cid}

@router.post("/continue_conversation", response_model=ContinueConversationResponse)
async def continue_conversation(req: ContinueConversationRequest):
    """
    Continue an existing conversation by its ID.
    """
    runner = get_runner_or_404(req.conversation_id)
    try:
        response = runner.get_response(req.prompt)
        return {"response": response}
    except HTTPException:
        raise

@router.post("/end_conversation", response_model=EndConversationResponse)
async def end_conversation(req: EndConversationRequest):
    """
    End a conversation, freeing resources.
    """
    runner = pop_runner_or_404(req.conversation_id)
    runner.stop_model()
    return {"status": "ended"}

@router.post("/change_model", response_model=ChangeModelRequest)
async def change_model(req: ChangeModelRequest):
    """
    Change the model for an existing conversation.
    """
    runner = pop_runner_or_404(req.conversation_id)
    runner.stop_model()
    runner.config["model_path"] = req.model_path
    runner.start_model()
    if not hasattr(runner, "model_instance") or runner.model_instance is None:
        raise to_http_exception(ModelLoadError(detail=ModelErrorDetailEnum.MODEL_INITIALIZATION_ERROR))
    new_cid = runner.model_instance.get_conversation_id()
    add_runner(new_cid, runner)
    return {"conversation_id": new_cid, "status": "model changed"}