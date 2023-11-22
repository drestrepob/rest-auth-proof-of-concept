from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str
    is_active: bool = True

    class Config:
        from_attributes=True


class DBUserSchema(UserSchema):
    hashed_password: str = Field(alias='password')
