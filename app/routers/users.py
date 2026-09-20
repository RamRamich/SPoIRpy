# app/routers/users.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.db import get_pool_conn

class UpdateUser(BaseModel):
    username: str = ""
    email: str = ""
    full_name: str = ""
    avatar_url: str = ""
    global_role: str = "user"
    default_role: str = ""

class CreateUser(BaseModel):
    username: str
    email: str
    full_name: str
    avatar_url: str = ""
    global_role: str
    default_role: str = ""
    hash_password: str
# Создаем экземпляр роутера.
# prefix="/users" — это пространство имен. Все маршруты в этом файле 
# автоматически получат этот префикс.
# tags=["Users"] — нужно для группировки в автоматической документации (Swagger UI).
router = APIRouter(prefix="/api/users",
                    tags=["Users"])


@router.get("") #
def get_users():
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return users 

@router.post("") #
def post_user(
    user: CreateUser
):
    conn = get_pool_conn() 
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, full_name, avatar_url, default_role, global_role) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user.username, user.email, user.password_hash, user.full_name, user.avatar_url,user.default_role,user.global_role)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}


@router.put("/{user_id}") # 
def update_user(
    user_id: int, user: UpdateUser
):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users "
            "SET username = %s, email = %s, full_name = %s, avatar_url = %s, default_role = %s, global_role = %s "
            "WHERE id = %s",
            (user.username, user.email, user.full_name, user.avatar_url, user.default_role,user.global_role ,user_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}

@router.delete("/{user_id}") # 
def delete_user(user_id: int):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}