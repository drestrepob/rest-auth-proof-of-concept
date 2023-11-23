from fastapi import Depends, FastAPI
from typing import Annotated

from app.auth.jwt import get_current_user
from app.schemas import UserSchema
from app.routers import (
    api_key_router, basic_router, bearer_router, digest_router, jwt_router, oauth2_router, user_router
)

app = FastAPI(
    title='auth API',
    description='An API to test several authentification methods',
    version='0.1.0',
)


@app.get('/')
async def home():
    return {
        'message': 'Welcome to my server!'
    }

@app.get('/me')
def me(current_user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    return current_user


# Routers
app.include_router(api_key_router)
app.include_router(basic_router)
app.include_router(bearer_router)
app.include_router(digest_router)
app.include_router(jwt_router)
app.include_router(oauth2_router)
app.include_router(user_router)
