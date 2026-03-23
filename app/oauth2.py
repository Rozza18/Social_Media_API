from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session

from . import models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #endpoint of our login

# three pieces: SECRET_KEY, ALGORITHM WE WANT TO USE, EXPIRATION TIME OF A TOKEN
SECRET_KEY = settings.secret_key
ALGOIRTHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() #make new copy of the data not to change/manipulate the original one
    expire_date = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # to let JWT tell us when it will be expired
    to_encode.update(
        {
            "exp": expire_date
        }
    )

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOIRTHM)
        return encoded_jwt
    except JWTError:
        raise

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGOIRTHM])

        id: str = payload.get("user_id") #type:ignore

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=int(id))

    except JWTError as e:
        print(e)
        raise credentials_exception
    except AssertionError as e:
        print(e)

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    token_data = verify_access_token(token, credentials_exception)

    #extract user_id from token_data
    user_id = token_data.id
    print(type(user_id))

    #fetching the user from database
    user = db.query(models.User).filter(models.User.id == user_id).first() #this shoud return a user model object
    return user