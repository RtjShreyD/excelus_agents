from pydantic import BaseModel

class InitializationRequest(BaseModel):
    session_id: str = None

class ChatRequest(BaseModel):
    session_id: str
    human_message: str

class MessageRequest(BaseModel):
    session_id: str
    query: str