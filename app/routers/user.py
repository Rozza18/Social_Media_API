from fastapi import status, HTTPException, Depends, APIRouter

from typing import List

from .. import models #to import our models
from ..database import  get_db
from ..schemas import UserCreate, UserOut

from sqlalchemy.orm import Session #to get the Session type passed to the route function
from ..utils import hash_password


router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

#users path operations
#get all users emails and when they were created
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if users is None:
        raise HTTPException(
            status_code=404,
            detail="No users found"
        )
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(
    user_request_body: UserCreate, db: Session = Depends(get_db)
):
    try:
        #hashing the password
        hashed_password = hash_password(user_request_body.password)
        user_request_body.password = hashed_password

        new_user = models.User(
                **user_request_body.model_dump()
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error While creating new user:{e}"
        )

@router.get("/{id}", status_code=200, response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    return user
