# app/routers/projects.py
from fastapi import APIRouter, Depends
from sqlmodel import Field, Session, SQLModel, create_engine

router = APIRouter(prefix="/api/projects", tags=["Projects"])
prefix="/projects"# — это пространство имен. Все маршруты в этом файле 
tags=["Projects"] #— нужно для группировки в автоматической документации (Swagger UI).


