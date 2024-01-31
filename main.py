from fastapi import FastAPI ,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request,name="index.html" , context={"name":"김태뿅"})


@app.get('/hello/{name}', response_class=HTMLResponse)
async def hello(request: Request , name):
    return templates.TemplateResponse(request=request,name="hello.html" , context={"name":name})