from pydantic import BaseModel


class Token(BaseModel):
    username: str
    token_type: str
    access_token: str
