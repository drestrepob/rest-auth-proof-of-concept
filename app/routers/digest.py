from fastapi import APIRouter, Depends

from app.auth.digest import validate_credentials


router = APIRouter(
    prefix='/digest',
    tags=['Digest'],
    dependencies=[Depends(validate_credentials)],
    responses={404: {'description': 'Not found'}},
)


@router.get('/greet')
async def poc_digest():
    return {
        'message': 'You are using a Digest auth to access this API!'
    }
