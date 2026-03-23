from fastapi import APIRouter, HTTPException, status, Depends

from ..schemas import Vote, GetVote

from .. import models, oauth2, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_remove_vote(
    vote: Vote,
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.get_current_user)
):
    """creating and removing votes on a post"""
    #retrieving the post to assure existence
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post with that id found!"
        )

    #check if the vote already existed
    found_vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
        )
    found_vote = found_vote_query.first()

    #depending on the vote direction, we will create (1) or remove (0)
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} already voted on this post {post.id}"
            )
        #creating a vote
        new_vote = models.Vote(
            user_id=current_user.id,
            post_id=post.id
        )
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote!"}
    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote is not already there"
            )
        found_vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote!"}

#get likes on specific post
@router.get("/get_post_votes")
def get_votes(
    vote: GetVote,
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.get_current_user)
):
    """when implementing we should get all votes and users voted on that post"""
    # # fetch count of votes from votes table with post_id
    # post_id = vote.post_id
    # if post_id is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No post found with that id." 
    #     )
    pass
