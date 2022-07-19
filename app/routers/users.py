from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..db import get_db


router = APIRouter(prefix='/users',
                   tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if(len(user.password) < 3):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password length is not long enough")

    # hash the password user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    existing_user = db.query(models.User).filter(
        models.User.email == new_user.email).first()

    if (existing_user and new_user.email == existing_user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"A user with this email: {new_user.email}")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print('Hello: ', new_user.id)
    new_user.access_token = oauth2.create_access_token(
        data={"user_id": new_user.id})
    new_user.token_type = "bearer"
    print(new_user.access_token)
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found")
    return users


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with id: {id}")
    return user
