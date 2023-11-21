from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.config import settings
from app.main import app

client = TestClient(app)


class TestBearerAuthentication:

    router_prefix = '/bearer'

    def test_protected_route_with_valid_token(self):
        path = f'{self.router_prefix}/greet'
        response = client.get(path, headers={'Authorization': f'Bearer {settings.BEARER_TOKEN}'})
        assert response.status_code == HTTP_200_OK
        assert response.json() == {'message': 'You are using a Bearer token to access this API!'}

    def test_protected_route_with_invalid_token(self):
        path = f'{self.router_prefix}/greet'
        response = client.get(path, headers={'Authorization': f'Bearer invalid'})
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Invalid authentication credentials'}
