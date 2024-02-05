from fastapi import FastAPI ,Request ,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from fastapi.responses import RedirectResponse
from passlib.hash import pbkdf2_sha256
from data import Articles

app = FastAPI()

#mongodb connect
mongodb_URI = "mongodb+srv://root:1234@ubion9.fcwrafy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongodb_URI)

db = client.ubion

templates = Jinja2Templates(directory="templates")
salt = "ubion"

@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request,name="index.html" , context={"name":"김태뿅"})


@app.get('/hello/{name}', response_class=HTMLResponse)
async def hello(request: Request , name ,action="훌라", sound: str = "빵빵"):
    print(f'action :{action} 그리고 소리 :{sound} ')
    return templates.TemplateResponse(request=request
                                      ,name="hello.html" 
                                      , context={"name":name 
                                                 , "action":action
                                                 , "sound":sound})
@app.get('/login', response_class=HTMLResponse)
async def login_page_view(request: Request ):
    return templates.TemplateResponse(request=request,name="login.html")


@app.post('/login', response_class=HTMLResponse)
async def login(request: Request, email:str=Form(...) , password:str=Form(...)):
    user = db.users
    user = user.find_one({"email":email })
    if user == None:
        return templates.TemplateResponse(request=request,name="register.html")
    else:
        result = pbkdf2_sha256.verify(password+salt, user['password'] )
        if result:
            return templates.TemplateResponse(request=request,name="index.html")
        else:
            return templates.TemplateResponse(request=request,name="login.html")
    

@app.get('/register', response_class=HTMLResponse)
async def login_page_view(request: Request ):
    return templates.TemplateResponse(request=request,name="register.html")

@app.post('/register',  response_class=HTMLResponse)
async def login(request: Request, username:str=Form(...) ,
                email:str=Form(...),
                phone:str=Form(...),
                password:str=Form(...)):
    users = db.users
    user = users.find_one({"email":email})
    if user == None:
        hashed_pw = pbkdf2_sha256.hash(password+salt)
        result = users.insert_one({
            "username":username,
            "email":email,
            "phone":phone,
            "password":hashed_pw
        })

        print(result)
        return templates.TemplateResponse(request=request,name="login.html" )

    else:
        return templates.TemplateResponse(request=request,name="register.html" )

@app.get('/list', response_class=HTMLResponse)
async def list(request: Request):
    # results = Articles()
    lists = db.lists
    results = lists.find()
    print(results)
    # return templates.TemplateResponse(request=request,name="list.html" , context={"list":results})
    return

@app.get('/create_list' , response_class=HTMLResponse)
async def create_list(request: Request):
    return templates.TemplateResponse(request=request,name="create_list.html")

import datetime

@app.post('/create_list', response_class=HTMLResponse)
async def create(request: Request ,
                 title:str=Form(...),
                 desc:str=Form(...),
                 author:str=Form(...),
                 ):
    lists = db.lists
    result = lists.insert_one({
            "title":title,
            "desc":desc,
            "author":author,
            "create_at":datetime.datetime.now()
        })
    print(result)
    return "SUCESS"
