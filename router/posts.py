from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, Query, APIRouter
from proj.access.schema import LinksRequest, UpdateLinksRequest, LinkResponse
from proj.access import model
from proj.access.database import get_db
from router.oauth2 import get_current_user

router = APIRouter(
    prefix= "/posts",
    tags= ["Links"]
)



@router.get("/", response_model=list[LinkResponse])
def get_posts(
        response: Response, db: Session = Depends(get_db),
        limit: int = Query(default=10, lt = 21),
        skip: int = Query(default=0),search: Optional[str] = "", current_user: int = Depends(get_current_user)
    ):
    post = db.query(model.Link).join(model.Link.owner).filter(
            model.Link.title.contains(search)
        ).offset(skip).limit(limit).all()
    response.status_code = status.HTTP_200_OK
    return post



@router.get("/{id}", response_model=LinkResponse)
def get_specific_post(id: int, response: Response, db: Session = Depends(get_db)
                        , current_user: int = Depends(get_current_user)):
    req_post =db.query(model.Link).filter(model.Link.id == id).first()
    if req_post == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
         detail= f"link with id:{id} does not exist")
    response.status_code = status.HTTP_200_OK
    return req_post



@router.post("/save", response_model = LinkResponse)
def save_Links(post:LinksRequest, response: Response, db: Session = Depends(get_db)
                , current_user: int = Depends(get_current_user)):
    new_post = model.Link(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_200_OK
    return new_post



@router.put("/{id}", response_model=LinkResponse)
def update_Links(id: int,updated_post:UpdateLinksRequest, response: Response, db: Session = Depends(get_db)
                    , current_user: int = Depends(get_current_user)):
    post_query= db.query(model.Link).filter(model.Link.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"link with id:{id} does not exist")

    # Owners can edit their own links; admins can edit any link.
    if post.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to Perform Requested Action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return post_query.first()



@router.delete("/delete/{id}")
def delete_Links(id: int, response: Response, db: Session = Depends(get_db),
                    current_user: int = Depends(get_current_user)):
    post_query = db.query(model.Link).filter(model.Link.id == id)
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"link with id:{id} does not exist")

    # Owners can delete their own links; admins can delete any link.
    if post.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to Perform Requested Action")

    post_query.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return{f"link with id:{id} has been deleted"}
