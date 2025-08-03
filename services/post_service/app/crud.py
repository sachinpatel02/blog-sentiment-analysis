from models import Post
from schemas import PostCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_post(post: PostCreate, session: AsyncSession, owner_id: int) -> Post:
    db_post = Post(**post.model_dump(), owner_id=owner_id)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post

