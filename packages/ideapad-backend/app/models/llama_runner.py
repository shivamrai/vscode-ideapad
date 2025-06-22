# We need to write a POST /chat handler and wire it to a stub model class in llama_runner.py.
#this is a class that will handle the llama model inference

from fastapi import HTTPException
from llama_cpp import Llama
import json
from pathlib import Path

class LlamaModel:
    def __init__(self, model_path: str):
        config_path = Path(__file__).resolve().parents[3] / "model_config.json"
        with open(config_path) as f:
            config = json.load(f)
        try:
            self.model_path = model_path
            self.n_ctx = config["n_ctx"]  # raises KeyError if missing
            self.temperature = config["temperature"]  # raises KeyError if missing
            self.max_tokens = config["max_tokens"]  # raises KeyError if missing

            self.model = Llama( model_path=self.model_path, n_ctx=self.n_ctx, temperature=self.temperature)
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Configuration missing: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")                          
       

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
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Initialize the model here (e.g., load the model from the path)
        # self.model = load_model(model_path)

    def run_inference(self, prompt: str) -> str:
        # This method should run inference on the model and return the response
        # For now, we will return a dummy response
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt must be a non-empty string")
        return self.get_response(prompt)
    
    def get_response(self, prompt: str) -> str:
        """
        Get a response from the model based on the provided prompt.
        This is a stub implementation that simulates a chat response.
        """
        # Pass the prompt to the model and get a response
        response = f"Response to: {prompt}"
        try:
            response = LlamaModel(self.model_path).generate_response(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")
        return response