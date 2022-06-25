from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from models.models import Author, User, LoginData
from persistency.persistency import read_users, read_authors, read_papers, create_author, create_user, \
    get_user_by_username, get_session, obter_usuario_logado
from utils.utils import create_hash, verify_hash, create_token, verify_token

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Projeto 001"}


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Healthy"}










