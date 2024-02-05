from fastapi import FastAPI ,Request ,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from fastapi.responses import RedirectResponse
from passlib.hash import pbkdf2_sha256
from data import Articles
from bson.objectid import ObjectId
from fastapi.staticfiles import StaticFiles
from fastapi import status
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
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
        return RedirectResponse(url="/register",status_code=status.HTTP_303_SEE_OTHER)
    else:
        result = pbkdf2_sha256.verify(password+salt, user['password'] )
        if result:
            return RedirectResponse(url="/",status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(url="/login",status_code=status.HTTP_303_SEE_OTHER)
    

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
        redirect_url = request.url_for('login')
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

    else:
        return templates.TemplateResponse(request=request,name="register.html" )
import asyncio
@app.get('/list', response_class=HTMLResponse)
async def list(request: Request):
    # results = Articles()
    result_list = []
    lists = db.lists
    results  = lists.find()
    # print(results)
    for i in results:
        result_list.append(i)
    return templates.TemplateResponse(request=request,name="list.html" , context={"list":result_list})
    

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
    return RedirectResponse(url="/list",status_code=status.HTTP_303_SEE_OTHER)

@app.get('/detail/{id}' , response_class=HTMLResponse)
async def details(request: Request , id):
    lists = db.lists
    result = lists.find_one({"_id":ObjectId(id)})
    print(result)
    return templates.TemplateResponse(request=request,name="detail.html" , context={"detail": result})

@app.get('/edit/{id}' , response_class=HTMLResponse)
async def details(request: Request , id):
    lists = db.lists
    result = lists.find_one({"_id":ObjectId(id)})
    print(result)
    return templates.TemplateResponse(request=request,name="edit.html" , context={"data": result})


@app.post('/edit/{id}', response_class=HTMLResponse)
async def create(request: Request , 
                 id,
                 title:str=Form(...),
                 desc:str=Form(...),
                 author:str=Form(...),
                 ):
    lists = db.lists
    lists.update_one(
            {'_id' : ObjectId(id)},
            {"$set": {
                "title":title,
                "desc" : desc,
                "author":author
            }},
            upsert=False

            )
    redirect_url = request.url_for('list')
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

@app.get('/delete/{id}')
def delete(request:Request , id):
    lists = db.lists
    lists.delete_one({"_id": ObjectId(id) })
    redirect_url = request.url_for('list')
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)