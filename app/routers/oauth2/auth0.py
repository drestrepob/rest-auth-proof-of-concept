from fastapi import APIRouter, Depends
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.oauth2.auth0 import retrieve_token, validate_token


router = APIRouter(
    prefix='/auth0',
    tags=['OAuth2'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/items')
async def get_items(valid_token: bool = Depends(validate_token)):
    return {
        'message': 'You are accessing these resources using Auth0!'
    }


@router.post('/token')
async def login_for_token():
    # Implement user validation
    token = retrieve_token(scope="items")
    return token
