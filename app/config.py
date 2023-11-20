from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API-KEY
    API_KEY: str
    API_KEY_NAME: str = 'access_token'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
