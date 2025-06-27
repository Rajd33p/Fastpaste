from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PasteCreate(BaseModel):
    content: str = Field(..., example="Hello from FastPaste!")
    expires_in: Optional[int] = Field(None, gt=0, example=3600)  # seconds, optional

class PasteResponse(BaseModel):
    slug: str
    content: str
    created_at: datetime
    expires_in: Optional[int]

    class Config:
        orm_mode = True
