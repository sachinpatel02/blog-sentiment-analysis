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

class PostUpdate(SQLModel):
    title: str | None = None
    content: str | None = None

class CommentBase(SQLModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentPublic(CommentBase):
    id: int
    created_at: datetime
    owner_id: int
    post_id: int
    #sentiment
    sentiment: str | None = None


#below is for returning a post with list of comments
class PostPublicWithComments(PostPublic):
    comments: list[CommentPublic] = []