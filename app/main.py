
from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

from random import randrange
from sqlalchemy.orm import Session
from . import models,schemas
from .database import get_db


import time

app = FastAPI()


# ระบบจะ validation ให้เลย 1. คือมี title กับ content ไหม , 2. เป็น type ตรงามที่กำหนดไหม    

# request Get method url: "/"



# ====== API Endpoints ======

@app.get("/") #เรียกว่า เดโคเรเดอร์ ทำให้ด้านใต้เป็น api
def root():
    return {"message" : "Welcome to my APIA"}     

# Query All post
@app.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Create post
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate ,db: Session= Depends(get_db)):
    # ** คือการแกะ dict ออกเป็น argument จะได้เป็น models.Post(title = "Hello", content = "World ") เป็นต้น
    # model.Post รับ dict ไมได้
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get lastest port
@app.get("/posts/latest",response_model=schemas.PostCreate)
def get_latest_post(db:Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return post


# Get Single Post
@app.get("/posts/{id}",response_model=schemas.PostCreate)
def get_post(id:int, db: Session = Depends(get_db) ):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    return post

# Delete
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return None

''' แต่ถ้าลอง delete แล้วไม่มี id อยู่จริงจะเกิด 500 ดังนั้นต้อง handle case  '''


@app.put("/posts/{id}",response_model=schemas.PostCreate)
def update_post(id:int, post_update: schemas.PostPut, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

@app.patch("/posts/{id}",response_model=schemas.PostCreate)
def update_post_patch(id:int, post_update: schemas.PostUpdate, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    # update เฉพาะส่วนที่ส่งมา
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)


    db.commit()
    db.refresh(post)
    return post


# title str, content str
# เวลา ทำ api order สำคัญมาก เอาพวก path แบบย่อยขึ้นก่อนเสมอ