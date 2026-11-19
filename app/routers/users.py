# # app/routers/users.py
from fastapi import APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine

router = APIRouter(prefix="/api/users", tags=["Users"])
prefix="/users"# — это пространство имен. Все маршруты в этом файле 
tags=["Users"] #— нужно для группировки в автоматической документации (Swagger UI).

