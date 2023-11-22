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

    # JWT
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRATION: int
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
