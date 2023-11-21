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

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
