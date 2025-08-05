from .models import Post, Comment
from .schemas import PostCreate, PostUpdate, CommentCreate
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


async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


###comments


async def create_comment(
    session: AsyncSession, comment_in: CommentCreate, owner_id: int, post_id: int
) -> Comment:
    comment_data = comment_in.model_dump()
    db_comment = Comment(**comment_data, owner_id=owner_id, post_id=post_id)
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return db_comment


async def create_comment_by_post_id(
    session: AsyncSession, post_id: int, skip: int = 0, limit: int = 100
) -> list[Comment]:
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())  # Show oldest comments first in the thread
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    return result.scalars().all()
