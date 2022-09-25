from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from proj.access.schema import TokenData
from sqlalchemy.orm import Session
from proj.access.database import get_db
from proj.access import model
import os




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRES_MINUTES = 55





def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,os.getenv("SECRET_KEY"),algorithm=os.getenv("ALG"))

    return encoded_jwt 



def verify_access_token(token:str, credentials_exception)-> str:
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALG"))  
        id: str = payload.get("user_id")  

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id) 
    except JWTError:
        raise credentials_exception 

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))-> dict:
    credentials_exception = HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail=f"Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
    ) 
    token = verify_access_token(token, credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    print(user)
    
    return user           

           

