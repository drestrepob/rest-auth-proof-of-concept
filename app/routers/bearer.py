from datetime import datetime, timedelta
from fastapi import APIRouter, Depends

from app.auth.bearer import authenticate_bearer, expiration
from app.config import settings


router = APIRouter(
    prefix='/bearer',
    tags=['Bearer'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/greet', dependencies=[Depends(authenticate_bearer)])
async def poc_basic():
    return {
        'message': 'You are using a Bearer token to access this API!'
    }


@router.get('/renew-token')
async def renew_token(token: str = Depends(authenticate_bearer)):
    global expiration
    expiration = datetime.now() + timedelta(seconds=30)
    return {
        'message': 'Token renewed!'
    }
