from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Annotated

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
class Post(SQLModel, table=True):
    id : Annotated[int | None, Field(default=None, primary_key=True)]
    title: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    owner_id: int = Field(foreign_key="user.id")
    