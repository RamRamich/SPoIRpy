from fastapi.templating import Jinja2Templates
from app.shellsort import shellSort

def second(request, templates: Jinja2Templates,arr):
    arr = arr.split(",")
    arr = shellSort(arr)
    data ={"arr" : arr}
    return templates.TemplateResponse(request, "second.html", data)