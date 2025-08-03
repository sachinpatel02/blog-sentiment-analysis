from datetime import datetime
from sqlmodel import SQLModel

class PostBase(SQLModel):
    title: str
    content: str


class PostCreate(PostBase):
    #no need to define anything as we have title and content from PostBase
    pass

class PostPublic(PostBase):
    id: int
    created_at: datetime
    owner_id: int
