from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, security
from ..database import get_session
import httpx

router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["comments"],
)


@router.post(
    "/", response_model=schemas.CommentPublic, status_code=status.HTTP_201_CREATED
)
async def create_a_comment(
    post_id: int,
    comment_in: schemas.CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user_id: int = Depends(security.get_current_user_id),
):
    """
    Create a new comment for a post.
    """
    # check if post exist
    post = await crud.get_post_by_id(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = await crud.create_comment(
        session=session,
        comment_in=comment_in,
        owner_id=current_user_id,
        post_id=post_id,
    )

    # ♻️🔆☑︎ callint sentiment service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8002/analyze",
                json={"text": new_comment.text},
            )
            response.raise_for_status()
            sentiment_data = response.json()
            sentiment = sentiment_data["sentiment"]

            if sentiment:
                new_comment.sentiment = sentiment
                await session.commit()
                await session.refresh(new_comment)
    except httpx.RequestError as e:
        print(f"Could not connect to sentiment service: {e}")

    return new_comment


@router.get("/", response_model=List[schemas.CommentPublic])
async def read_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieve comments for a specific post.
    """
    post = await crud.get_post_by_id(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = await crud.create_comment_by_post_id(
        session=session, post_id=post_id, skip=skip, limit=limit
    )
    return comments
