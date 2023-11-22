from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    expires_at: float


class TokenData(BaseModel):
    email: str
    username: str
