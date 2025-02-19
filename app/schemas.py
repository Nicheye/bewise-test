from pydantic import BaseModel
from datetime import datetime


class ApplicationBase(BaseModel):
    user_name: str
    description: str


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationOut(ApplicationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
