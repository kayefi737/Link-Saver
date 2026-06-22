from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from proj.access import utils
from proj.access.schema import  UserCreate, UserResponse, RoleUpdate
from proj.access import model
from proj.access.database import get_db
from router.oauth2 import require_admin


router = APIRouter(
    prefix="/user",
    tags= ["Users"]
)




@router.get("/",response_model=list[UserResponse])
def get_allusers(response: Response, db: Session = Depends(get_db),
                 current_admin = Depends(require_admin)):
    all_users = db.query(model.User).all()
    response.status_code = status.HTTP_200_OK
    return all_users




@router.get("/{id}",response_model=UserResponse)
def get_user(id:int, response:Response, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f"User with id:{id} does not exist")
    response.status_code = status.HTTP_200_OK
    return user


@router.post("/create", response_model=UserResponse)
def create_user(user:UserCreate, response:Response, db: Session = Depends(get_db)):
    #hashed password - user password
    hashed_password = utils.hash(user.password)
    new_user = model.User(
        email=user.email,
        password=hashed_password,
        role=utils.role_for_email(user.email),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.status_code = status.HTTP_200_OK
    return new_user


@router.put("/{id}/role", response_model=UserResponse)
def set_user_role(id: int, payload: RoleUpdate, response: Response,
                  db: Session = Depends(get_db),
                  current_admin = Depends(require_admin)):
    user_query = db.query(model.User).filter(model.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist")
    user_query.update({"role": payload.role}, synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return user_query.first()


@router.delete("/delete/{id}")
def delete_user(id: int, response: Response, db: Session = Depends(get_db),
                current_admin = Depends(require_admin)):
    user = db.query(model.User).filter(model.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
              detail= f"User wit id:{id} does not exist")
    user.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return{f"User with id:{id} has been deleted"}
