from faker import Faker
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.auth.digest import calculate_digest_response
from app.config import settings
from app.main import app

client = TestClient(app)
fake = Faker()


class TestDigestAuthentication:

    router_prefix = "/digest"

    def test_protected_route_with_valid_digest_credentials(self):
        path = f"{self.router_prefix}/greet"
        digest_response = calculate_digest_response(
            username=settings.DIGEST_USERNAME,
            password=settings.DIGEST_PASSWORD,
            realm=settings.DIGEST_REALM,
            nonce=settings.DIGEST_NONCE,
            uri=path
        )
        headers = {
            "Authorization": f'Digest username="{settings.DIGEST_USERNAME}", realm="{settings.DIGEST_REALM}", nonce="{settings.DIGEST_NONCE}", uri="{path}", response="{digest_response}"'
        }
        response = client.get(path, headers=headers)
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"message": "You are using a Digest auth to access this API!"}

    def test_protected_route_with_invalid_digest_credentials(self):
        path = f'{self.router_prefix}/greet'
        headers = {
            "Authorization": f'Digest username="{fake.name()}", realm="{settings.DIGEST_REALM}", nonce="{fake.word()}", uri="{path}", response="{fake.sha1()}"'
        }
        response = client.get(path, headers=headers)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Incorrect username or password"}

    
