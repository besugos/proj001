import uuid
from datetime import datetime

from fastapi import HTTPException, status, Depends

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import APIRouter
from typing import Optional
from fastapi import Query
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from models.models import User, LoginData
from persistency.persistency import read_users, create_user, get_user_by_username, get_user_info
from utils.utils import verify_token, create_hash, verify_hash, create_token, get_token_expiry

from starlette.requests import Request


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@limiter.limit("5/minute")
async def get_users(request: Request, current_user=Depends(get_user_info)):
    users = read_users()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
def post_user(user: User, request: Request, current_user: object = Depends(get_user_info)):
    if 'type' in current_user:
        if current_user['type'] == 'admin':
            password = create_hash(user.password)
            created_user = create_user(user.type, password, user.username)
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

    token = create_token({'sub': user['username'], 'aut': user['type']})

    return {"user": user, "token": token['token'], 'expires at': token['exp'].strftime("%d/%m/%Y %H:%M")}


@router.post("/me")
async def me(user=Depends(get_user_info)):
    return user


@router.get("/expiry")
async def expiry(exp=Depends(get_token_expiry)):
    if 'Error' in exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired Token')
    return {'Token expires at': exp}
