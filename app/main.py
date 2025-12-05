from fastapi import Body, FastAPI
from random import randrange
from .database import get_db, engine, Base
import time
from .routers import post, user, auth


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Welcome to my API"}     

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


