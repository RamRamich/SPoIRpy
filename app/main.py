from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.index import index
from app.db import get_pool_conn
from app.routers import users
from app.routers import tasks
from app.routers import projects


app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(projects.router)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index_route(request: Request):
    return index(request, templates)





