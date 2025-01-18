from pydantic import BaseModel, ConfigDict

class ContactCreate(BaseModel):
    username: str

class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    contact_id: int
    username: str
    nickname: str
