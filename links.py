from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends 
from proj.access import model
from dotenv import load_dotenv, find_dotenv
from proj.access.database import engine,get_db
from router import posts, users, auth
from pydantic import BaseSettings

load_dotenv(find_dotenv(".env")) 

class Settings(BaseSettings):
    DATABASE_PASSWORD: str = "localhost"
    DATABASE_USERNAME: str = "postgres"



model.Base.metadata.create_all(bind=engine) 

app = FastAPI()

    

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router) 


@app.get("/")
def root():
    return {"message": "Dark World"}


@app.get("/sqlalchemy")
def test_links(db: Session = Depends(get_db)):
    
    post = db.query(model.Link).all()
    return post 
                 


          







        

         



       







    





           