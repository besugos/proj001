import uuid

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import persistency.user_persistency
from models.models import User
# from persistency.user_persistency import get_user_by_username
from utils.utils import verify_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def get_session():
    engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/projeto001")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_engine():
    engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/projeto001")
    return engine


def get_id():
    myuuid = str(uuid.uuid1().int)
    id = int((myuuid[0:3]) + (myuuid[(len(myuuid) - 4):len(myuuid)]))
    return id


def rows_as_dicts(cursor):
    """convert tuple result to dict with cursor"""
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]


def get_user_info(token: str = Depends(oauth2_schema)):
    try:
        username: str = verify_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    user = persistency.user_persistency.get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    return user

