from .models import Post
from .schemas import PostCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


async def create_post(post: PostCreate, session: AsyncSession, owner_id: int) -> Post:
    db_post = Post(**post.model_dump(), owner_id=owner_id)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post


# let's get posts: We are using Pagination here
# Pagination: We do not want to send all posts in single request, because it's slow
# we will send fewer posts


async def get_posts(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[Post]:
    statement = select(Post).order_by(Post.id.desc()).offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()



async def get_post_by_id(session: AsyncSession, post_id:int) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
