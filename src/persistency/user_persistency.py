import uuid

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from persistency.persistency_utils import get_session, rows_as_dicts, get_engine
from src.persistency.persistency_utils import rows_as_dicts, get_session, get_engine


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')



def read_users():
    session = get_session()
    query = 'SELECT * FROM proj001.user'
    cursor = session.execute(query).cursor
    users: object = rows_as_dicts(cursor)
    return users


def get_user_by_username(username: str):
    session = get_session()
    query = f'''SELECT * FROM proj001.user WHERE username = '{username}' '''
    cursor = session.execute(query).cursor
    users = rows_as_dicts(cursor)
    if len(users) > 0:
        user = users[0]
    else:
        user = []
    return user


def create_user(type: str, username: str, password: str):
    engine = get_engine()
    query = f'''INSERT INTO proj001.user (type, username, password) VALUES ('{type}', '{username}', '{password}') RETURNING user_id, username, type'''
    result = engine.execute(query)
    created_user = result.fetchone()
    return created_user

