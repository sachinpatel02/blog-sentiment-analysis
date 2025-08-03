from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .models import User
from .schemas import UserCreate
from .security import get_password_hash

#Create User
async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user_data = user_in.model_dump(exclude={"password"})
    hashed_password = get_password_hash(user_in.password)
    db_user = User(**user_data, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

#Get User by email id
async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()