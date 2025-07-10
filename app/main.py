from fastapi import FastAPI
from passlib.context import CryptContext
from . import models
from .database import engine
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware
# Importing necessary modules and packages

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#models.Base.metadata.create_all(bind=engine) # not needed with alambic

# Initializing the FastAPI application
# This is the main entry point of the application
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Including routers for posts and users
# This allows the application to handle requests related to posts and users
app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)
   
# Root endpoint
# This endpoint returns a simple JSON response with a message
@app.get("/")
def root():
    return {"message": "Hello World"}