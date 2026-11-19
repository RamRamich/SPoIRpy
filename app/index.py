from fastapi.templating import Jinja2Templates
from datetime import datetime

def index(request, templates: Jinja2Templates):
    today = datetime.now()
    data = {
        "name": "Дима",
        "date": str(today)
    }

    return templates.TemplateResponse(request, "index.html", data)