from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, security

from .. database import get_session

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post(
    "/", response_model=schemas.PostPublic, status_code=status.HTTP_201_CREATED
)
async def create_new_post(
    post_in: schemas.PostCreate,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(security.get_current_user_id),
):
    new_post = await crud.create_post(
        post=post_in, session=session, owner_id=current_user_id
    )
    return new_post


@router.get("/", response_model=list[schemas.PostPublic])
async def read_posts(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrive pages with pagination

    """
    posts = await crud.get_posts(session=session, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.PostPublic)
async def read_post(post_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a single post by its ID.
    """
    db_post = await crud.get_post_by_id(session=session, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post