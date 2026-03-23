from .database import engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models

from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine) #to create our models when the app is starting


# creating instance of fastapi
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or use ["*"] for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# path operation - route  in some other languages-
@app.get("/") # decorator
def root(): #async/sync plain function
    return {
        "message": "Welcome to my API!"
    } #fastapi automatically converts python dictionary to JSON and send to the client
