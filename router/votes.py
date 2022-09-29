from fastapi import Response, status, HTTPException, Depends,APIRouter
from proj.access.database import get_db
from sqlalchemy.orm import Session
from proj.access.schema import Vote
from proj.access import model
from router.oauth2 import get_current_user




router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/")
def vote(vote:Vote, response:Response, db: Session = Depends(get_db),
      current_user: int = Depends(get_current_user) ):
      post = db.query(model.Link).filter(model.Link.id == vote.post_id).first()
      if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail= "Link with id:{id} does not exist")

      vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id,
                             model.Vote.user_id == current_user.id)
      found_vote = vote_query.first()                       
      if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"user{current_user.id} already voted on post")
        new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit() 
        response.status_code = status.HTTP_200_OK   
        return{"message": "successfully voted"}

      else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link with id:{id} does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()       
                           


    