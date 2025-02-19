from sqlalchemy import Column, Integer,String

from database import Base


class User(Base):
    __tablename__="Users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    age = Column(Integer,nullable=True)
    