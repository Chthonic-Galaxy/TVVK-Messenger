from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class MessageCreate(BaseModel):
    recipient_username: str
    content: str

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    sender_username: str
    content: str
    timestamp: datetime
