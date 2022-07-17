from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.schemas import UserLogin, UserOut
from sqlalchemy.orm import Session
from app import models, oauth2
from app.database import get_db
from app.utils import password_hash


router = APIRouter(tags=['Users'])


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserLogin, db: Session = Depends(get_db)):
    # hash the password- user.password
    hashed_password = password_hash(user.password)

    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')

    return user
