import os
import json
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_routes
from app.employees import router as employee_routes
from app.employees.utils import add_fake_employee, add_fake_employee_state
from app.users import router as user_routes
from app.users.utils import create_superuser, create_fake_users
from app.database import create_db_and_tables


ORIGINS: list = json.loads(os.getenv("ORIGINS"))  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    add_fake_employee()
    add_fake_employee_state()
    create_superuser()
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
api.include_router(employee_routes.router)
api.include_router(user_routes.router)


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
