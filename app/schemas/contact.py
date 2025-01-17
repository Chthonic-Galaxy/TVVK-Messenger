from pydantic import BaseModel, ConfigDict

class ContactCreate(BaseModel):
    contact_id: int

class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    contact_id: int
