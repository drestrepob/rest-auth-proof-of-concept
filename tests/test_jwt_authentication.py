from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.config import settings
from app.database import base, get_db
from app.main import app

fake = Faker()
engine = create_engine(settings.TEST_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


class TestBasicAuthentication:
    jwt_router_prefix = '/jwt'
    user_router_prefix = '/users'

    def _create_user(self, username: str, password: str):
        path = f'{self.user_router_prefix}/'
        response = client.post(
            path,
            json={
                'username': username,
                'password': password,
            }
        )
        assert response.status_code == HTTP_200_OK
        return response.json()

    def test_protected_route_with_valid_jwt(self):
        test_username = fake.user_name()
        test_password = fake.word()
        self._create_user(test_username, test_password)
        path = f'{self.jwt_router_prefix}/token'
        response = client.post(
            path,
            data={
                'username': test_username,
                'password': test_password,
            }
        )
        assert response.status_code == HTTP_200_OK
        access_token = response.json()['access_token']
        response = client.get(
            '/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        assert response.status_code == HTTP_200_OK

    def test_protected_route_with_invalid_jwt(self, invalid_jwt):
        response = client.get(
            '/me',
            headers={'Authorization': f'Bearer {invalid_jwt}'}
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED
