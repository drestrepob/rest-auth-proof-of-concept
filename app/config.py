from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API-KEY
    API_KEY: str
    API_KEY_NAME: str

    # Basic
    BASIC_USERNAME: str
    BASIC_PASSWORD: str

    # Bearer
    BEARER_TOKEN: str

    # Database
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    # Digest
    DIGEST_USERNAME: str
    DIGEST_PASSWORD: str
    DIGEST_NONCE: str
    DIGEST_REALM: str

    # JWT
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRATION: int
    JWT_SECRET_KEY: str

    # Auth0
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_DOMAIN: str
    AUTH0_ISSUER: str
    AUTH0_AUDIENCE: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
