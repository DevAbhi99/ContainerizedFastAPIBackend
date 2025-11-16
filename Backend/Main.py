from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from enum import IntEnum
from contextlib import asynccontextmanager
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration - supports both local and Docker MySQL
dbHost = os.getenv("DB_HOST")
dbPort = os.getenv("DB_PORT")  # Use 3307 for Docker
dbUser = os.getenv("DB_USER")
dbPassword = os.getenv("DB_PASSWORD")
dbName = os.getenv("DB_NAME")

password = quote_plus(dbPassword)

mysql_url = f'mysql+pymysql://{dbUser}:{password}@{dbHost}:{dbPort}/{dbName}'

engine=create_engine(mysql_url, echo=True)


#add middleware

api=FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_headers=["*"],
    allow_methods=["*"]
)

api.add_middleware(
    GZipMiddleware, minimum_size=1000
)

class Priority(IntEnum):
    high=3
    medium=2
    low=1


class Users(SQLModel, table=True):
    __tablename__='users'
    id:int|None=Field(default=None, primary_key=True)
    name:str=Field(nullable=False)
    age:int=Field(nullable=False)
    priority:Priority=Field(nullable=False)


#Get method

@api.get('/getData')
def getMethod():
    with Session(engine) as session:
        users=session.exec(select(Users)).all()
        return users

#post method
@api.post('/sendData')
def postMethod(newUser:Users):
    with Session(engine) as session:
        session.add(newUser)
        session.commit()
        session.refresh(newUser)
        return {'message':'Data inserted successfully'}

#put method
@api.put('/updateData/{id}')
def putMethod(id:int, newUser:Users):
    with Session(engine) as session:
        user=session.get(Users, id)

        if not user:
            raise HTTPException(status_code=404, detail='Wrong input')

      
        user.name=newUser.name
        user.age=newUser.age
        user.priority=newUser.priority

        session.add(user)
        session.commit()
        session.refresh(user)
        return {'message':'Data updated successfully'}


#delete method

@api.delete('/deleteData/{id}')
def deleteMethod(id:int):
    with Session(engine) as session:
        users=session.get(Users, id)
        if not users:
            raise HTTPException(status_code=404, detail="wrong input")
        
        session.delete(users)
        session.commit()
        return {'message':'Data deleted successfully'}


#clear method

@api.delete('/clearData')
def clearMethod():
    with Session(engine) as session:
        
        session.exec(text('truncate table users;'))
        session.commit()
        return {'message':'Data cleared successfully'}

 