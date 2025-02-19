from fastapi import FastAPI, HTTPException,Depends,status
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

@app.get('/user/{id}')
def get_user_by_id(id,db:Session=Depends(get_db)):
    return db.query(models.User).filter(models.User.id==id).first()

@app.delete('/user/{id}')
def delete(id,db:Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail='No such record found')        
    db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
    db.commit()
    return {'message':'Successfully deleted record'}

@app.put('/update-user/{id}')
def update(id,request:UserSchema,db:Session = Depends(get_db)):
    
    user=db.query(models.User).filter(models.User.id==id)

    if not user:
        raise HTTPException(status_code=404,detail='No such record found')
    
    user.update(request.model_dump())
    db.commit()
    return {'message':'Operation Successfull'}


   