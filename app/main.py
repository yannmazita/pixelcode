import os
import json
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_routes
from app.clients import router as client_routes
from .routers import users
from .database import create_db_and_tables
from .models import create_fake_users, create_admin_user


ORIGINS: list = json.loads(os.getenv("ORIGINS"))  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_admin_user()
    create_fake_users()
    yield


api = FastAPI(lifespan=lifespan)

api.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.include_router(auth_routes.router)
api.include_router(users.router)
api.include_router(client_routes.router)


def start_server():
    uvicorn.run(
        "app.main:api",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
    # when reload=true, the 1st argument the location of main as module and a string
    # ie: "app.main:api"


if __name__ == "__main__":
    start_server()
