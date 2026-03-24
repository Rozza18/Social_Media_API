"""posts router file contains all required operation paths for posts"""
from fastapi import Response, status, HTTPException, Depends, APIRouter

from typing import List, Optional

from .. import models #to import our models
from ..database import  get_db #import engine and sessionlocal
from ..schemas import PostCreate, Post, TokenData, PostWithVote

from ..oauth2 import get_current_user

from sqlalchemy import or_, func
from sqlalchemy.orm import Session #to get the Session type passed to the route function

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)



#posts path operations


@router.get("/", response_model=List[PostWithVote])
# @router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
    ):
    """get all posts with keyword/search/limit queries and votes added"""
    print(limit)
    # posts = db.query(models.Post).filter(
    #     or_(
    #         models.Post.title.ilike(f"%{search}%"),
    #         models.Post.content.ilike(f"%{search}%")
    #         )).limit(limit=limit).offset(skip).all() #enable us to search the DB with keywords
    # print(posts)
    posts_votes = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id,
            isouter=True).group_by(models.Post.id).filter(
        or_(
            models.Post.title.ilike(f"%{search}%"),
            models.Post.content.ilike(f"%{search}%")
            )).limit(limit=limit).offset(skip).all()
    print(posts_votes)
    return posts_votes

#return our only posts
@router.get("/my_posts", response_model=List[PostWithVote])
def get_own_posts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """get own posts like for own personal profile"""
    own_posts = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")).join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()
    if not own_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found for that user"
        )
    return own_posts

@router.get("/{id}", response_model=PostWithVote)#to fetch specific post using path parameter, it is string here not integer
def get_specififc_post(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)): #this can be used to internally convert extracted str parameter to an integer id
    """gets specific post with id"""
    fetched_post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")).join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(fetched_post)
    if not fetched_post:
        raise HTTPException(
            status_code=404,
            detail=f"post with id: {id} was not found"
        )
    return fetched_post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Post)#sending some data in the request body
def create_posts(
    request_body: PostCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) #creating a dependecy to make sure that user doing the request is authenticated
):
    """create post operation path"""
    print(f"user_id: {current_user.id}")
    print(f"user_email: {current_user.email}")

    print(f"{request_body.model_dump()}")
    new_post = models.Post(
        **request_body.model_dump(), owner_id=current_user.id #double * unpacking the post model to title, content, published, and created at automaticalluy
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    """delete post operation path"""
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(
            status_code=404,
            detail=f"post with id {post_id} not found."
        )
    
    if post.first().owner_id != current_user.id: #type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden to delete this post!"
        )
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


#updating posts - send the data that we want it to be updated
@router.put("/{id}", response_model=Post)
def update_post(id: int, post_info: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist!"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden to update that post!"
        )

    post_query.update(
        {
            'title': post_info.model_dump()['title'],
            'content': post_info.model_dump()['content'],
            'published': post_info.model_dump()['published'],
        }, synchronize_session=False
    ) #this can be converted to post_query.update(post_info.model_dump(), sync..etc)
    db.commit() #pushing the changes to postgres server
    db.refresh(post) #resave the updated data into the post variable to be returned
    return post
