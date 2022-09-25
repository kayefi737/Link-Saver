from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os



outh2_scheme = OAuth2PasswordBearer(tokenUrl= "token")
userDetail ={'username':'olly', 'password':'playrank247'}


def create_token(data: dict, duration_in_hrs: Union[float, int]) -> str:
    expire = datetime.utcnow() + timedelta(minutes= (duration_in_hrs * 60))
    data["exp"] = expire
    print(os.getenv("ALG"))
    encoded_jwt = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALG"))
    return encoded_jwt 


async def get_user_from_token(token: str = Depends(outh2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.removeprefix("Bearer "), os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALG")])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return payload