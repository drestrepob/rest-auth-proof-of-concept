from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.config import settings
from app.main import app

client = TestClient(app)


class TestBasicAuthentication:

    router_prefix = '/basic'
    
    def test_protected_route_with_valid_credentials(self):
        path = f'{self.router_prefix}/greet'
        response = client.get(path, auth=(settings.BASIC_USERNAME, settings.BASIC_PASSWORD))
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'You are using a Basic (user & password) to access this API!'}

    def test_protected_route_with_invalid_credentials(self):
        path = f'{self.router_prefix}/greet'
        response = client.get(path, auth=('invalid', 'invalid'))
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Incorrect username or password'}
