from fastapi import APIRouter, Depends

from app.auth.auth0 import get_clients, retrieve_token, validate_token


router = APIRouter(
    prefix='/auth0',
    tags=['OAuth2'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/clients')
async def get_clients(clients: list[dict] = Depends(get_clients)):
    return clients


@router.get('/resources')
async def get_items(valid_token: dict = Depends(validate_token)):
    return {
        'message': 'You are accessing these resources using Auth0!',
        'payload': valid_token
    }


@router.post('/token')
async def login_for_token():
    token = retrieve_token()
    return token
