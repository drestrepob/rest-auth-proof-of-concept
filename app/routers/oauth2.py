from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Annotated

from app.auth.oauth2 import retrieve_token, validate_token
from app.config import settings


router = APIRouter(
    prefix='/oauth2',
    tags=['OAuth2'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/auth0/items')
async def get_items(valid_token: bool = Depends(validate_token)):
    return {
        'message': 'Hello World!'
    }


@router.post('/auth0/token')
async def login_for_token():
    # Implement user validation
    token = retrieve_token(scope="items")
    return token
