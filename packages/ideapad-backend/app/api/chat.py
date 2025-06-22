# app/api/chat.py

from fastapi import APIRouter, HTTPException
from app.models.llama_runner import LlamaRunner
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "model_config.json"
with open(CONFIG_PATH) as f:
    config = json.load(f)

MODEL_PATH = config["model_path"]

router = APIRouter()

# Temporary runner; in production use DI or singleton
runner = LlamaRunner(model_path=MODEL_PATH)

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/model_info")
async def model_info():
    """
    Get information about the model.
    Returns the model path and other relevant details.
    """
    return {
        "model_path": runner.model_path,
        "description": "Llama model for inference",
        "version": "1.0.0"
    }

@router.post("/user_query")
async def user_query(prompt: str):
    """
    Handle user queries.
    Calls LlamaRunner to perform inference.
    """
    try:
        response = runner.run_inference(prompt)
        return {"response": response}
    except HTTPException as e:
        raise e