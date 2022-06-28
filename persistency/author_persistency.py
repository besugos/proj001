import uuid

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import User
from persistency.persistency_utils import get_session, rows_as_dicts, get_engine
from utils.utils import verify_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def read_authors(name: str = None):
    session = get_session()
    query = 'SELECT * FROM proj001.author'
    if name is not None:
        query = query + f" WHERE LOWER(name) LIKE LOWER('%{name}%')"
    cursor = session.execute(query).cursor
    authors = rows_as_dicts(cursor)
    return authors


def read_author_by_id(author_id: int):
    session = get_session()
    query = f'''SELECT * FROM proj001.author WHERE author_id = {author_id}'''
    cursor = session.execute(query).cursor
    authors = rows_as_dicts(cursor)
    return authors


def create_author(name: str, picture: str):
    engine = get_engine()
    query = f'''INSERT INTO proj001.author (name, picture) VALUES ('{name}', '{picture}') RETURNING author_id, name, picture'''
    result = engine.execute(query)
    created_author = result.fetchone()
    return created_author
