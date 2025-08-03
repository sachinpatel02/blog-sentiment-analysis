from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import post_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- Post Service: Lifespan event startup ---")
    await init_db()
    yield
    print("--- Post Service: Lifespan event shutdown ---")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post_routes.router)