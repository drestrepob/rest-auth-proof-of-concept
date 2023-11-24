import httpx
import logging

from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from okta_jwt.jwt import validate_token
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import settings

logger = logging.getLogger(__name__)
security = OAuth2PasswordBearer(tokenUrl='/okta/token', scheme_name='OAuth2')


def retrieve_token(authorization, scope: str):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': scope,
        'audience': settings.OKTA_AUDIENCE
    }
    url = f"{settings.OKTA_ISSUER}/v1/token"
    response = httpx.post(url, headers=headers, data=data)
    if response.status_code == httpx.codes.OK:
        logger.error(f"OKTA response: {response.json()}")
        return response.json()
    else:
        logger.error(f"Error retrieving token: {response.text}")
        raise HTTPException(status_code=400, detail=response.text)


class OktaTokenValidator(ABC):
    """
    Abstract class for validating Okta tokens
    """
    @abstractmethod
    def validate(self, token: str = Depends(security)):
        pass


class OktaTokenValidatorOffline(OktaTokenValidator):
    """
    Validates Okta tokens offline. This method is slightly less secure because 
    you can't be sure that the access token hasn't been revoked remotely, but 
    on the other hand, you don't have to use your Okta client secret to 
    validate the token locally.
    """
    def validate(self, token: str = Depends(security)):
        try:
            response = validate_token(
                token,
                settings.OKTA_ISSUER,
                settings.OKTA_AUDIENCE,
                settings.OKTA_CLIENT_ID
            )
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'}
            )


class OktaTokenValidatorOnline(OktaTokenValidator):
    """
    Validates Okta tokens online. The Okta authorization server's /inspect 
    endpoint to check the token. The advantage of this method is that you will 
    know if the token has been revoked; the downside is that it's slower than 
    validating the JWT locally.
    """
    def validate(self, token: str = Depends(security)):
        headers = {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        }
        data = {
            "client_id": settings.OKTA_CLIENT_ID,
            "client_secret": settings.OKTA_CLIENT_SECRET,
            "token": token,
        }
        url = settings.OKTA_ISSUER + '/v1/introspect'
        response = httpx.post(url, headers=headers, data=data)
        if response.status_code == httpx.codes.OK:
            logger.error(f"OKTA response: {response.json()}")
            is_active = response.json()['active']
            if not is_active:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail='Invalid user',
                    headers={'WWW-Authenticate': 'Bearer'}
                )
            return
        
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
