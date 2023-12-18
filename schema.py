from typing import Optional, List
from pydantic import BaseModel

class ThreadResponse(BaseModel):
    thread_id: str


class MessageRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None

class MessageResponse(BaseModel):
    thread_id: str
    run_id: str
    message_id: str

class StatusResponse(BaseModel):
    status: str
    error_message: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

class RetrieveResponse(BaseModel):
    messages: List[Message]
