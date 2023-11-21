from fastapi import APIRouter, Depends, HTTPException

from app.auth.basic import validate_credentials


router = APIRouter(
    prefix='/basic',
    tags=['Basic'],
    dependencies=[Depends(validate_credentials)],
    responses={404: {'description': 'Not found'}},
)


@router.get('/greet')
async def poc_basic():
    return {
        'message': 'You are using a Basic (user & password) to access this API!'
    }
