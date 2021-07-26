from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Server(BaseModel):
    id: Optional[int] = Field(alias='_id')
    name: str = None
    status: str = None
    description: str = None
    url: str = None
    updatedDate: str = None


class Status(str, Enum):
    ACTIVE = 'active'

