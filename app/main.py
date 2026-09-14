from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.index import index
from app.first import first
from app.second import second
from app.third import third

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index_route(request: Request):
    return index(request, templates)

@app.get("/first")
async def first_route(request: Request, art: str = ""):
    return first(request, templates,art)

@app.get("/second")
async def second_route(request: Request, arr: str = "err"):
    return second(request, templates,arr)

@app.get("/third")
async def third_route(request: Request, command: str = ""):
    return third(request, templates,command)