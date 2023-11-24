import pytest

from datetime import datetime, timedelta
from faker import Faker
from jose import jwt

fake = Faker()


@pytest.fixture(autouse=True, scope="session")
def invalid_jwt():
    user_id = fake.uuid4()
    expiration_time = datetime.utcnow() + timedelta(minutes=1)
    payload = {
        "sub": str(user_id),
        "exp": expiration_time,
        "iat": datetime.utcnow(),
        # Add any other claims you need in your JWT
    }
    secret_key = fake.word()
    fake_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
    return fake_jwt
