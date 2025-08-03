from fastapi import FastAPI
from .database import init_db
from contextlib import asynccontextmanager
import sys
from .routers import user_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- Lifespan event: Application startup ---")
    try:
        await init_db()
        yield
    except Exception as e:
        print(f"FATAL ERROR: Application startup failed: {e}")
        sys.exit("Could not initialize the database. Exiting application.")
    finally:
        print("--- Lifespan event: Application shutdown ---")


app = FastAPI(lifespan=lifespan)
app.include_router(user_routes.router)