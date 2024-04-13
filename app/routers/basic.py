from fastapi import APIRouter, Depends
from starlette import status

from app.auth.basic import validate_credentials


router = APIRouter(
    prefix='/basic',
    tags=['Basic'],
    dependencies=[Depends(validate_credentials)],
    responses={status.HTTP_404_NOT_FOUND: {'description': 'Not found'}},
)


@router.get('/greet')
async def poc_basic():
    return {
        'message': 'You are using a Basic (user & password) to access this API!'
    }
