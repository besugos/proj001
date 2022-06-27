import uuid

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import User
from persistency.persistency_utils import get_session, rows_as_dicts
from utils.utils import verify_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def read_papers(name: str = None):
    session = get_session()
    query = 'SELECT * FROM proj001.paper'
    if name is not None:
        query = query + f" WHERE LOWER(name) LIKE LOWER('%{name}%')"
    cursor = session.execute(query).cursor
    papers = rows_as_dicts(cursor)
    return papers
