from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware 
from proj.access import model
from dotenv import load_dotenv, find_dotenv
from proj.access.database import engine,get_db
from router import posts, users, auth, votes



load_dotenv(find_dotenv(".env")) 



model.Base.metadata.create_all(bind=engine) 

app = FastAPI()

origins= ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router) 


@app.get("/")
def root():
    return {"message": "Dark World"}


@app.get("/sqlalchemy")
def test_links(db: Session = Depends(get_db)):
    
    post = db.query(model.Link).all()
    return post 
                 


          







        

         



       







    





           