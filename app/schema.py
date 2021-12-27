from pydantic import BaseModel
from typing import Optional, Any

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    name: str
    password: str

class TaskResult(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None

class Task(BaseModel):
    task_id: str