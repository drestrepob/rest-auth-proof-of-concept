import httpx
import logging

from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

logger = logging.getLogger(__name__)
jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
security = OAuth2PasswordBearer(tokenUrl=f"https://{settings.AUTH0_DOMAIN}/oauth2/default/v1/token")


def retrieve_token(scope: str):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.AUTH0_CLIENT_ID,
        "client_secret": settings.AUTH0_CLIENT_SECRET,
        "audience": settings.AUTH0_AUDIENCE
    }
    logger.error(f"URL {settings.AUTH0_ISSUER}/oauth/token")
    response = httpx.post(url=f"{settings.AUTH0_ISSUER}/oauth/token", headers=headers, data=data)
    if response.status_code == 200:
        logger.error(f"AUTH0 response:")
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
            headers={"WWW-Authenticate": "Bearer"}
        )


async def validate_token(token: str = Depends(security)):
    json_url = httpx.get(jwks_url)
    jwks = json_url.json()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    try:
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
    except KeyError:
        logger.exception("Unable to verify token!")
        raise HTTPException(
            status_code=401,
            detail="Unable to verify token!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AUTH0_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
        except jwt.ExpiredSignatureError:
            logger.exception("Token signature expired!")
            raise HTTPException(
                status_code=401,
                detail="Token signature expired!",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except jwt.JWTClaimsError:
            logger.exception("Incorrect claims, please check the audience and issuer!")
            raise HTTPException(
                status_code=401,
                detail="Incorrect claims, please check the audience and issuer!",
                headers={"WWW-Authenticate": "Bearer"}
            )
        else:
            # Logic to validate scope or user data
            return True
  
    return False
