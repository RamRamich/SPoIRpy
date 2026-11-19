# app/db.py
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
import os

# 1. Получаем URL базы данных из переменных окружения (из docker-compose)
# Если переменной нет (например, при локальном запуске), используем дефолтную
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://user:password@db:3306/appDB"
)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# 4. Зависимость (Dependency) для получения сессии в эндпоинтах FastAPI
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session