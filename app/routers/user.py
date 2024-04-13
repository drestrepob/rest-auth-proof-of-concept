from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import DBUserSchema, UserSchema


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/', response_model=UserSchema)
def create_user(user: DBUserSchema, db: Session = Depends(get_db)):
    return User.create(db, **user.model_dump())


@router.get('/', response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return User.get_all(db)


@router.get('/{username}', response_model=UserSchema)
def get_user(username: str, db: Session = Depends(get_db)):
    return User.get(db, username)
