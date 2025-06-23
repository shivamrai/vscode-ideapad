# Pydantic schemas
from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str

class StartConversationResponse(BaseModel):
    conversation_id: str

class ContinueConversationRequest(BaseModel):
    conversation_id: str
    prompt: str

class ContinueConversationResponse(BaseModel):
    response: str

class EndConversationRequest(BaseModel):
    conversation_id: str

class EndConversationResponse(BaseModel):
    status: str