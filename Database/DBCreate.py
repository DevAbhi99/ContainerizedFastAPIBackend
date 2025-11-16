from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine
from enum import IntEnum
from contextlib import asynccontextmanager
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


load_dotenv()

dbpassword=os.getenv('DB_PASSWORD')

password=quote_plus(dbpassword)

mysql_url=f'mysql+pymysql://root:{password}@localhost:3306/fastapidb'


engine=create_engine(mysql_url, echo=True)

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


SQLModel.metadata.create_all(engine)