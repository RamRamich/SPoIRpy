from fastapi.templating import Jinja2Templates
import subprocess

def third(request, templates: Jinja2Templates,command):
    if "rm" in command:
        return templates.TemplateResponse(request, "third.html", {"arr":["please not rm"]})
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        data = {"arr": result.stdout.split("\n")}
    except:
        data ={"arr" : ["err"]}
    return templates.TemplateResponse(request, "third.html", data)