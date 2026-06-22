from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint, validator

class LinksRequest(BaseModel):
    title: str
    content: str
    rated_18: Optional[bool] = False



class UpdateLinksRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rated_18: Optional[bool] = False

class UserResponse(BaseModel):
    id:int
    email: EmailStr
    role: str
    created_at: datetime


    class Config:
        orm_mode= True

class LinkResponse(BaseModel):
    id:int
    title: str
    content: str
    rated_18: Optional[bool] = False
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class RoleUpdate(BaseModel):
    role: str

    @validator("role")
    def role_must_be_valid(cls, v):
        allowed = {"user", "admin"}
        if v not in allowed:
            raise ValueError(f"role must be one of {sorted(allowed)}")
        return v


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
