from pydantic import BaseModel


class Account(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True


class AccountCreate(BaseModel):
    email: str
    username: str
    password: str


class AccountLogin(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
