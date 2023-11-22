from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Annotated

from app.auth.jwt import authenticate_user, create_access_token, refresh_token
from app.config import settings
from app.database import get_db
from app.schemas import TokenSchema


router = APIRouter(
    prefix='/jwt',
    tags=['JWT'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/token')
async def login_for_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenSchema:
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
        },
        expires_delta=expires_at
    )
    return TokenSchema(
        access_token=access_token,
        token_type='bearer',
        expires_at=expires_at.total_seconds(),
    )


@router.post('/token/refresh')
def refresh_access(
    refreshed_token: str = Depends(refresh_token),
) -> TokenSchema:
    expires_at = timedelta(minutes=settings.JWT_TOKEN_EXPIRATION)
    return TokenSchema(
        access_token=refreshed_token,
        token_type='bearer',
        expires_at=expires_at.total_seconds(),
    )
