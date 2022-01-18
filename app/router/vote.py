from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.sql.functions import mode
from .. import database, oauth2, schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote', tags=['VOTE'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    if (vote.dir == 1):
       
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Already voted for post {vote.post_id}")
        
        vote_row = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(vote_row)
        db.commit()
        
        return {"message": "Sucessfully added vote!"}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Vote not found for post {vote.post_id}")
        
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {"message": "Sucessfully removed vote!"}
    