from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Annotated

from app.auth.jwt import authenticate_user, create_access_token
from app.config import settings
from app.database import get_db


router = APIRouter(
    prefix='/jwt',
    tags=['JWT'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/token')
async def login_for_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    authenticated_user = authenticate_user(db, form_data.username, form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    expires_at = timedelta(minutes=settings.JWT_TOKEN_EXPIRATION)
    access_token = create_access_token(
        data={
            'sub': authenticated_user.username,
            'is_active': authenticated_user.is_active,
        }
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_at': expires_at,
    }
