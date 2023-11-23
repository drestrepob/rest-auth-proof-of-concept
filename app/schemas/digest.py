from pydantic import BaseModel
from typing import Optional, Self


class HTTPDigestCredentials(BaseModel):
    username: str
    realm: str
    nonce: str
    uri: str
    response: str
    opaque: Optional[str] = None
    algorithm: str = "MD5"
    qop: Optional[str] = None
    nc: Optional[str] = None
    cnonce: Optional[str] = None

    @classmethod
    def from_string_credentials(cls, credentials: str) -> Self:
        credentials_dict = {}
        parts = credentials.split(",")
        for part in parts:
            key, value = map(str.strip, part.split("=", 1))
            credentials_dict[key] = value.strip('"')

        return cls(**credentials_dict)
