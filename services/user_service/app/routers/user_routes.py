# services/user_services/app/routers/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# CORRECTED: Use relative imports with '..' to go up one directory level
from .. import crud, schemas, security
from ..database import get_session

# Create the router with a prefix and tags for better organization
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# 1. create user
@router.post(
    "/",  # The path is now just "/", which maps to "/users/" because of the prefix
    response_model=schemas.UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: schemas.UserCreate, session: AsyncSession = Depends(get_session)
):
    """
    Endpoint to register a new user.
    Required Fields:
    1. username: str
    2. email: str
    3. password: str
    """
    db_user = await crud.get_user_by_email(session=session, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = await crud.create_user(session=session, user_in=user_in)

    return new_user


# 2. token creation
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Endpoint for login
    Required Fields:
    1. username: str -- your email id
    2. password: str
    """
    user = await crud.get_user_by_email(session=session, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# 3. me
@router.get("/me", response_model=schemas.UserPublic)
async def read_users_me(
    current_user: schemas.UserPublic = Depends(security.get_current_user),
):
    """
    Endpoint to return user details
    1. username: str
    2. email: str
    3. id: int
    """
    return current_user