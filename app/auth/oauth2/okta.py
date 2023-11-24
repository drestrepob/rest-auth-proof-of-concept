import httpx
import logging

from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
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
    Validates Okta tokens offline.
    """
    def validate(self, token: str = Depends(security)):
        pass


class OktaTokenValidatorOnline(OktaTokenValidator):
    """
    Validates Okta tokens online.
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
