from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    user_id: int = None
    type: str
    username: str
    password: str


class Author(BaseModel):
    author_id: int = None
    name: str
    picture: str


class Paper(BaseModel):
    paper_id: int = None
    category: str
    title: str
    summary: str
    first_paragraph: str
    body: str
    author_id: int


class LoginData(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


