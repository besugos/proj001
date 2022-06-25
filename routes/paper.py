from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from models.models import Author, User, LoginData
from persistency.persistency import read_users, read_authors, read_papers, create_author, create_user, \
    get_user_by_username, get_session, obter_usuario_logado
from utils.utils import create_hash, verify_hash, create_token, verify_token

from fastapi import APIRouter
from typing import Optional
from fastapi import Query

router = APIRouter(
    prefix="/paper",
    tags=["Paper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_papers():
    papers = read_papers()
    return papers
