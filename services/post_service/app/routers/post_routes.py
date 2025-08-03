from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, security
from database import get_session

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

