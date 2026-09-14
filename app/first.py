from fastapi.templating import Jinja2Templates


def first(request, templates: Jinja2Templates,art):
    if art.isnumeric():
        art = int(art)
    else:
        art=0
    if art & 1:
        color ="red"
    else:
        color = "green"
    if art & 2:
        size = 50
    else:
        size = 100
    if art & 4:
        shape = f'<rect x="10" y="10" width="{size}" height="{size}" stroke="{color}" fill="transparent" stroke-width="5"/>'
    else:
        shape = f'<circle cx="100" cy="100" r="{size/2}" fill="{color}"/>'
    data = f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">{shape}</svg>'

    return templates.TemplateResponse(request, "first.html", {"svg":data})