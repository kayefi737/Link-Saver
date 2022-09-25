from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URL'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    while True: 
     try:
         conn = psycopg2.connect( host="localhost", database="links_db", user="postgres", password="Kayefi",
         cursor_factory=RealDictCursor)
         cur = conn.cursor()
         print("Database Connection Was Successful!")
         break
     except Exception as error:
         print("Connection to Database Failed")
         print({"Error": error})
         time.sleep(3)        