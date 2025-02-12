from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

db_url = os.getenv('MONGODB_URI')

client = MongoClient(db_url)


new_db = client["new_db"]  

users_collection = new_db["users"]

class User(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: str | None
    age: str | None



@app.get('/users')
def users():
  all_users=users_collection.find()
  all_users=list(all_users)
  for user in all_users:
      user['_id']=str(user['_id'])
  return all_users
@app.post('/users/add_new_user')
async def add_new_user(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail='User already exists')

 
    new_user = user.model_dump()
    result = users_collection.insert_one(new_user)

    new_user["_id"] = str(result.inserted_id) 
    print('User successfully added!')
    return {"message": "User successfully added", "user": new_user}

@app.patch('/users/update_user')
def update_user(email,update:UserUpdate):
    updated_field={}
    if email is None:
        raise HTTPException(status_code=400,detail='Please enter the email')
    if update.name and update.age is None:
        raise HTTPException(status_code=400,detail='Please Provide a value for update')
    if update.name:
        updated_field['name']=update.name
    if update.age:
        updated_field['age']=update.age
    
    users_collection.update_one({'email':email},{'$set':updated_field})

@app.delete('/users/delete_user')
def delete_user(email):
    if not email:
        raise HTTPException(status_code=400, detail="Please provide an email")
    deleted_user = users_collection.find_one_and_delete({"email": email})
    if deleted_user is None:
        raise HTTPException(status_code=400,detail='User does not Exist')
    return 'Opeation successfull'

