from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    messages: str = Field(..., description = "User's incomming message.")