from passlib.context import CryptContext

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

def hash_password(raw_password: str):
    return pwd_context.hash(raw_password)

def verify(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)