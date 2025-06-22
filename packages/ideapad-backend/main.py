# FastAPI Backend Entry


from fastapi import FastAPI
from app.api import chat


app = FastAPI(
    title="Ideapad Backend",
    description="Backend for the Ideapad application",
    version="0.1.0")


#_Register routes
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Ideapad Backend!"}


#a POST /chat handler and wire it to a stub model class in llama_runner.py.

@app.post("/api/chat")
async def chat_handler(prompt: str):
    """
    Handle chat requests.
    This is a stub implementation that simulates a chat response.
    """
    if not prompt:
        return {"error": "Prompt cannot be empty"}
    
    # Simulate a response from the model
    response = f"Response to: {prompt}"
    
    return {"response": response}