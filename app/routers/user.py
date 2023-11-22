from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.auth.jwt import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import DBUserSchema, UserSchema


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/')
def create_user(user: DBUserSchema, db: Session = Depends(get_db)) -> UserSchema:
    return User.create(db, **user.model_dump())


@router.get('/')
def get_users(db: Session = Depends(get_db)) -> List[UserSchema]:
    return User.get_all(db)


@router.get('/{username}')
def get_user(username: str, db: Session = Depends(get_db)) -> UserSchema:
    return User.get(db, username)


@router.get('/me')
def me(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    return {
        'message': 'You are logged in!'
    }
