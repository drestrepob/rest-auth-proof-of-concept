from fastapi import APIRouter, Depends
from starlette import status

from app.auth.api_key import get_api_key


router = APIRouter(
    prefix='/api-key',
    tags=['Api Key'],
    dependencies=[Depends(get_api_key)],
    responses={status.HTTP_404_NOT_FOUND: {'description': 'Not found'}},
)


@router.get('/greet')
async def poc_api_key():
    return {
        'message': 'You are using an API KEY to access this API!'
    }
