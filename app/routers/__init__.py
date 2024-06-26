from .api_key import router as api_key_router
from .basic import router as basic_router
from .bearer import router as bearer_router
from .digest import router as digest_router
from .jwt import router as jwt_router
from app.routers.auth0 import router as auth0_router
from .user import router as user_router
