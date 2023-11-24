from fastapi import APIRouter, Depends, Request
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Annotated

from app.auth.oauth2.okta import OktaTokenValidator, OktaTokenValidatorOffline, OktaTokenValidatorOnline, retrieve_token


router = APIRouter(
    prefix='/okta',
    tags=['OAuth2'],
    responses={404: {'description': 'Not found'}},
)
offline_validator = OktaTokenValidatorOffline()
online_validator = OktaTokenValidatorOnline()


@router.post('/token')
def login(request: Request):
    authorization = request.headers.get('Authorization')
    token = retrieve_token(authorization=authorization, scope="username")
    return token


@router.get('/username')
def get_username(valid_token: bool = Depends(online_validator.validate)):
    return {
        'message': 'Hello World!'
    }
