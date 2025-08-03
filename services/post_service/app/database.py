import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ FATAL: DATABASE_URL environment variable not set in .env file")


engine = create_async_engine(
    DATABASE_URL, echo=True, connect_args={"statement_cache_size": 0}
)


async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def init_db():
    print("♻️ Attempting to initialize database....")
    try:
        await create_db_and_tables()
        print("✅ Database and tables checked/created successfully")
    except Exception as e:
        print(f"❌ An error occurred during database initialization: {e}")
        raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
