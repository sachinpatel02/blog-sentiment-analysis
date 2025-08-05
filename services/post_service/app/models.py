from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    #Relationship for ORM
    posts: list["Post"] = Relationship(back_populates="owner")
    comments: list["Comment"] = Relationship(back_populates="owner")
    
class Post(SQLModel, table=True):
    id : Annotated[int | None, Field(default=None, primary_key=True)]
    title: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    owner_id: int = Field(foreign_key="user.id")

    #Relationship for ORM
    owner: User = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")

class Comment(SQLModel, table=True):
    id : Annotated[int | None, Field(default=None, primary_key=True)]
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    #foreign keys
    owner_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")

    #Relationship for ORM
    owner: User = Relationship(back_populates="comments")
    post: Post = Relationship(back_populates="comments")