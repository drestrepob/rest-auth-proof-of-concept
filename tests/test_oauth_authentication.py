from faker import Faker
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.auth.oauth2.auth0 import retrieve_token
from app.config import settings
from app.main import app

client = TestClient(app)
fake = Faker()


class TestOAuthAuthentication:

    auth0_router_prefix = '/auth0'
    okta_router_oprefix = '/okta'
    
    def test_protected_route_with_valid_credentials(self):
        path = f'{self.auth0_router_prefix}/items'
        token = retrieve_token(scope="items")
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        response = client.get(path, headers=headers)
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'You are accessing these resources using Auth0!'}

    def test_protected_route_with_invalid_credentials(self, invalid_jwt):
        path = f'{self.auth0_router_prefix}/items'
        headers = {"Authorization": f"Bearer {invalid_jwt}"}
        response = client.get(path, headers=headers)
        assert response.status_code == HTTP_401_UNAUTHORIZED
