from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TodoBase(BaseModel):
    title: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime | str
    updated_at: datetime | str

    model_config = ConfigDict(from_attributes=True)
