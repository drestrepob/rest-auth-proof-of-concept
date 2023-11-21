from fastapi import APIRouter, Depends, HTTPException

from app.auth.api_key import get_api_key


router = APIRouter(
    prefix='/api-key',
    tags=['Api Key'],
    dependencies=[Depends(get_api_key)],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def poc_api_key():
    return {
        'message': 'You are using an API KEY to access this API!'
    }
