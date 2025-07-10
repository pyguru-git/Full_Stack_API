from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session 
from .. import models, schemas,oauth2
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
# This router handles the CRUD operations for posts
# It includes endpoints to create, read, update, and delete posts
# The endpoints are defined with appropriate HTTP methods and response models
# The router is used to group related endpoints together for better organization
# The endpoints are prefixed with "/posts" to indicate they are related to posts
# The router also includes dependency injection for the database session and current user
# The current user is obtained using the oauth2.get_current_user dependency
# The database session is obtained using the get_db dependency  

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user),
search :Optional[str]= ""):

     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).all()
     return posts
    

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post : schemas.PostCreate,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

   
    # Create a new post instance using the PostCreate schema
    new_post = models.Post(user_id=current_user.id  ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest",response_model=schemas.Post)
def get_post(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    # latest_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).order_by(models.Post.id.desc()).first()

    # Retrieve the latest post from the database
    # The latest post is determined by ordering the posts by their ID in descending order   
    # If no posts are found, raise a 404 Not Found exception
    # If a post is found, return it as a response       
    if not latest_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No posts found")
    return latest_post



@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
     #post = db.query(models.Post).filter(models.Post.id == id).first()

     post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

     if not post:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
     return post


@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first():
        if delete_post.first().user_id == current_user.id:
        # If the post exists and belongs to the current user, delete it
        # The synchronize_session=False argument is used to avoid issues with the session state
            delete_post.delete(synchronize_session=False)
            db.commit()
        else:
             raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f'Not authorised to perfor the requested action')
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
    # If the post was deleted successfully, return a 204 No Content response
    # No content is returned in the response body
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,post :schemas.PostUpdate, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post:
        if updated_post.user_id != current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f'Not authorised to perform the requested action')
        # If the post exists and belongs to the current user, update it
        # The post data is converted to a dictionary and each field is updated
        # The synchronize_session=False argument is used to avoid issues with the session state
        else:
            updated_post_query.update(post.dict(), synchronize_session=False)
            
            db.commit()
            db.refresh(updated_post)
        # If the post was updated successfully, return the updated post
        # The updated post is returned as a response    
         # Return the updated post
        return updated_post
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')
   
