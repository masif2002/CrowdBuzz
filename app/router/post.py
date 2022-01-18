from os import stat
from typing import List, Optional
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import func
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
    )

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), 
posts_limit: int = 100, posts_skip: int = 0, search: str = ""):
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(posts_limit).offset(posts_skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).order_by(models.Post.id).filter(models.Post.title.contains(search)).limit(posts_limit).offset(posts_skip).all()   
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # Returns 201 which is the status code supposed to be returned with POST method according to the convention
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()


    new_post = models.Post(**post.dict(), user_id=current_user.id) # Unpacks the dictionary and sets in the format as the line above
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Retrieve the new post and store it into new_post. Similar to RETURNING * in sql

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
#@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):# id: int tells FastAPI to validate the received id to be an integer
    # cursor.execute("SELECT * FROM posts WHERE id = %s;", (str(id),))
    # post = cursor.fetchone()

    #ost = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post: #If post is not found (which returns None)
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    

    if not post: 
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform selected action")


    # If post exists, we delete it
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): #With PUT method, we need to send in all the fields. So we get all the fields
   
    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *;", (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform selected action")
    
    # If post exists
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post

