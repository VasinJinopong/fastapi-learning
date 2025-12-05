from .. import models, schemas, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )

# Query All post
@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)  ):
    posts = db.query(models.Post).all()
    return posts

# Create post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate ,db: Session= Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
    # ** คือการแกะ dict ออกเป็น argument จะได้เป็น models.Post(title = "Hello", content = "World ") เป็นต้น
    # model.Post รับ dict ไมได้

    print(current_user.email)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get lastest port
@router.get("/latest",response_model=schemas.PostCreate)
def get_latest_post(db:Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return post


# Get Single Post
@router.get("/{id}",response_model=schemas.PostCreate)
def get_post(id:int, db: Session = Depends(get_db) ):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    return post

# Delete
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return None

''' แต่ถ้าลอง delete แล้วไม่มี id อยู่จริงจะเกิด 500 ดังนั้นต้อง handle case  '''


@router.put("/{id}",response_model=schemas.PostCreate)
def update_post(id:int, post_update: schemas.PostPut, db:Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

@router.patch("/{id}",response_model=schemas.PostCreate)
def update_post_patch(id:int, post_update: schemas.PostUpdate, db:Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
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
