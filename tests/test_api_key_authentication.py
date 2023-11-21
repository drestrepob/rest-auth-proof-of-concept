from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.config import settings
from app.main import app

client = TestClient(app)


class TestApiKeyAuthentication:

    router_prefix = '/api-key'

    def test_protected_route_with_valid_api_key(self):
        path = f'{self.router_prefix}/greet'
        response = client.get(path, headers={settings.API_KEY_NAME: settings.API_KEY})
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'You are using an API KEY to access this API!'}

    def test_protected_route_with_invalid_api_key(self):
        path = f'{self.router_prefix}/greet'
        response = client.get(path, headers={settings.API_KEY_NAME: 'invalid'})
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate API KEY'}
