import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import SQLAlchemyError

# 1. loading doenv
load_dotenv()

# 2. fetching db_url from .env. If not find any url, railse an error
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# 3. create asynchronous engine
engine = create_engine(DATABASE_URL, echo=True)


# 5. logic for db & table creation
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# 6. initializing database
def init_db():
    print("♻️ Attepmting to initialize database....")
    try:
        create_db_and_tables()
        print("✅ Database and tables checked/created successfully")
    except SQLAlchemyError as e:
        print(f"❌ An error occurred during async database initialization: {e}")
        raise


# 7. returning session objects to make changes in database
def get_session():
    with Session(engine) as session:
        yield session
