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
    paper_id: int
    category: str
    title: int
    summary: str
    firstParagraph: str
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


