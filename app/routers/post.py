from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter

from typing import Optional, List
from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import mode
from .. import models, schemas, utils, oauth2
from ..db import get_db

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.Post])
# def get_posts():
# cursor.execute("""SELECT * FROM posts""")
# posts = cursor.fetchall()
def get_posts(db: Session = Depends(get_db), current_user: dict = Depends((oauth2.get_current_user)), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).all()
    # To only retrieve posts that only the user made use the following code
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found")
    return posts


@router.get('/{id}', response_model=schemas.Post)
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
#     post = cursor.fetchone()
def get_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends((oauth2.get_current_user))):
    get_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not get_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found")

    # # To keep the user posts only visible to that user
    # if get_post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    return get_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: Post):
# cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
#                (post.title, post.content, post.published))
# new_post = cursor.fetchone()
# conn.commit()
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends((oauth2.get_current_user))):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(
#         """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
#     index = cursor.fetchone()
#     conn.commit()
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
# def update_post(id: int, post: Post):
#     cursor.execute(
#         """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends((oauth2.get_current_user))):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
