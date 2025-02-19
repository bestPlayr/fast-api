from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
import models
from database import engine,SessionLocal
import models
from schemas import UserSchema
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/')
def new():
    return {'message':'hi'}

@app.post('/create-user')
def create_user(user:UserSchema, db:Session = Depends(get_db)):
    new_user=models.User(name=user.name,email=user.email,age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users-list')
def users_list(db:Session = Depends(get_db)):
    result=db.query(models.User).all()
    return result

    