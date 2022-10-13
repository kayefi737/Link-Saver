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
    #cur.execute("""SELECT * FROM links LIMIT {limit}, {skip};""" )
    #Links = cur.fetchall()
    #conn.commit()
    #post = db.query(model.Link).filter(model.Link.owner_id == current_user.id).all()
    '''@router.get("/join")
    def join(db:Session = Depends(get_db)):
    posts = db.query(model.Link).filter(model.Link.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(model.Link).join(model.Vote, model.Vote.post_id == model.Link.id, isouter=True)
    print(result)'''
    print(current_user)
    post = db.query(model.Link).join(model.Link.owner).filter(
            model.Link.title.contains(search)
        ).offset(skip).limit(limit).all() 
    response.status_code = status.HTTP_200_OK 
    return post 



@router.get("/{id}", response_model=LinkResponse)
def get_specific_post(id: int, response: Response, db: Session = Depends(get_db)
                        , current_user: int = Depends(get_current_user)):
    # cur.execute("""SELECT * FROM links WHERE id = %s """, (id,) )
    # Links = cur.fetchone()
    print(current_user)
    req_post =db.query(model.Link).filter(model.Link.id == id).first()
    if req_post == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
         detail= f"link with id:{id} does not exist")
    response.status_code = status.HTTP_200_OK
    return req_post 

   

@router.post("/save", response_model = LinkResponse)
def save_Links(post:LinksRequest, response: Response, db: Session = Depends(get_db)
                , current_user: int = Depends(get_current_user)):
    # cur.execute("""INSERT INTO links(title, content,rated_18) VALUES(%s,%s,%s)""",
    #         (post.title,post.content,post.rated_18 or "false"))
    # cur.execute("""SELECT * FROM links ORDER BY created_at DESC LIMIT 1;""")
    # new_post= cur.fetchall()
    # conn.commit()
    # response.status_code = status.HTTP_200_OK
    #First way below 
    #new_post = model.Link(title=post.title, content= post.content,
    #             rated_18= post.rated_18)
    print(current_user.id)
    new_post = model.Link(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)             
    response.status_code = status.HTTP_200_OK             
    return new_post 
   


@router.put("/{id}", response_model=LinkResponse)
def update_Links(id: int,updated_post:UpdateLinksRequest, response: Response, db: Session = Depends(get_db)
                    , current_user: int = Depends(get_current_user)):
    # cur.execute("""UPDATE links SET title = %s, content = %s, rated_18 = %s WHERE id = %s""",
    #             (post.title,post.content,post.rated_18 or "false", (id,) ))
    # cur.execute("""SELECT * FROM links WHERE id = %s;""", (id,))            
    # updated_post = cur.fetchone()
    # print(updated_post)
    # conn.commit()
    print(current_user)
    post_query= db.query(model.Link).filter(model.Link.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"link with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to Perform Requested Action")    

    post_query.update(updated_post.dict(), synchronize_session=False)  
    db.commit()    
    response.status_code = status.HTTP_200_OK
    return post_query.first()                
    


@router.delete("/delete/{id}")
def delete_Links(id: int, response: Response, db: Session = Depends(get_db), 
                    current_user: int = Depends(get_current_user)):
    # cur.execute("""DELETE FROM links WHERE id = %s""", (id,))
    # deleted_post = cur.fetchone()
    # conn.commit()
    print(current_user)
    post_query = db.query(model.Link).filter(model.Link.id == id)
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"link with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to Perform Requested Action") 

    post_query.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return{f"link with id:{id} has been deleted"}