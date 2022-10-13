import psycopg2
from psycopg2.extras import RealDictCursor
import time 

class Env:
    security = {}


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