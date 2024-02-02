from pymongo import MongoClient
import json

# 방법1 - URI
mongodb_URI = "mongodb+srv://root:1234@ubion9.fcwrafy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongodb_URI)

# 방법2 - HOST, PORT
# client = MongoClient(host='localhost', port=27017)

db = client.ubion
data = db.users
# print(client.list_database_names())

# data.insert_one({
#     "username":"park",
#     "password":"5678"
# })

# cursor = data.find({"username":"kimk"})
# print(list(cursor))

# cursor_1 = data.find_one({"email":"1@naver.com"})
# if cursor_1 == None:
#     print("sssssss")
# else:
#     print(cursor_1)

from passlib.hash import pbkdf2_sha256
salt = 'ubion'
# print(pbkdf2_sha256.hash("1234"))
result = pbkdf2_sha256.hash("1234"+salt)
# if pbkdf2_sha256.verify("1234"+salt,result, ):
#     print("fewfewfwefwe")
print(pbkdf2_sha256.verify("ewfew"+salt, result ))
