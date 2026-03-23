from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..utils import verify

from .. import models

from ..database import get_db

from .. import oauth2

from ..schemas import Token

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=Token)
def login( response: Response, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_email = user_credentials.username
    user_password = user_credentials.password

    if user_email is None or user_password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request, Make sure that u have written your email and password"
        )

    #get the user from database
    user = db.query(models.User).filter(models.User.email == user_email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    if not verify(user_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    #creating a token and return it with the response body
    response.status_code = status.HTTP_200_OK
    return Token(
        access_token=access_token,
        token_type="Bearer"
    )
