import uuid

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import APIRouter
from typing import Optional
from fastapi import Query

from models.models import User, LoginData
from persistency.persistency import read_users, create_user, get_user_by_username, obter_usuario_logado
from utils.utils import verify_token, create_hash, verify_hash, create_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_users():
    users = read_users()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_authors(user: User):
    password = create_hash(user.password)
    created_user = create_user(user.type, user.username, password)
    return created_user


@router.post("/token")
async def login(login_data: LoginData):
    password = login_data.password
    username = login_data.username
    user = get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong credentials')

    valid_password = verify_hash(password, user['password'])

    if not valid_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong credentials')

    token = create_token({'sub': user['username']})

    return {"user": user, "token": token}


@router.post("/me")
async def me(user=Depends(obter_usuario_logado)):
    return user
