# We need to write a POST /chat handler and wire it to a stub model class in llama_runner.py.
#this is a class that will handle the llama model inference

from fastapi import HTTPException



class LlamaRunner:
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Initialize the model here (e.g., load the model from the path)
        # self.model = load_model(model_path)

    def run_inference(self, prompt: str) -> str:
        # This method should run inference on the model and return the response
        # For now, we will return a dummy response
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        return f"Response to: {prompt}"