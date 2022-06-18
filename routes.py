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


@app.get("/users")
async def get_users():
    users = read_users()
    return users


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def post_authors(user: User):
    password = create_hash(user.password)
    created_user = create_user(user.type, user.username, password)
    return created_user


@app.get("/authors")
async def get_authors(name: str = None):
    authors = read_authors(name)
    return authors


@app.post("/authors", status_code=status.HTTP_201_CREATED)
async def post_authors(author: Author, user=Depends(obter_usuario_logado)):
    if not user:
        return user
    created_author = create_author(author.name, author.picture)
    return created_author


@app.get("/papers")
async def get_papers():
    papers = read_papers()
    return papers


@app.post("/token")
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


@app.post("/me")
async def me(user=Depends(obter_usuario_logado)):
    return user


