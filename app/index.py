from fastapi.templating import Jinja2Templates


def index(request, templates: Jinja2Templates):
    data = {
        "name": "Иван",
        "date": "11 сентября 2026"
    }
    return templates.TemplateResponse(request, "index.html", data)