from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from models.models import Author, User, LoginData
from persistency.persistency import read_users, read_authors, read_papers, create_author, create_user, \
    get_user_by_username, get_session, get_user_info
from utils.utils import create_hash, verify_hash, create_token, verify_token

from fastapi import APIRouter
from typing import Optional
from fastapi import Query

router = APIRouter(
    prefix="/author",
    tags=["Author"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_authors(name: str = None, user=Depends(get_user_info)):
    authors = read_authors(name)
    return authors


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_authors(author: Author, user=Depends(get_user_info)):
    if 'type' in user:
        if user['type'] == 'admin':
            created_author = create_author(author.name, author.picture)
            return created_author
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
