# services/user_services/app/database.py

import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. Load the DATABASE_URL from your .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ FATAL: DATABASE_URL environment variable not set in .env file")


# 2. Create the Asynchronous Engine
# THIS IS THE CRITICAL FIX: The 'connect_args' dictionary tells the asyncpg driver
# to disable the prepared statement cache, which is required to work with
# Supabase's pgbouncer connection pooler.
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"statement_cache_size": 0}
)


# 3. Create the Async Session Maker
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# 4. Database Initialization and Session Logic
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