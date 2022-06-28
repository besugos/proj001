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

def read_papers(title: str = None):
    session = get_session()
    query = 'SELECT * FROM proj001.paper'
    if title is not None:
        query = query + f" WHERE LOWER(title) LIKE LOWER('%{title}%')"
    cursor = session.execute(query).cursor
    papers = rows_as_dicts(cursor)
    return papers


def create_paper(title: str, category: str, summary: str, first_paragraph: str, body: str, author_id: int):
    engine = get_engine()
    query = f'''INSERT INTO proj001.paper (title, category, summary, first_paragraph, body, author_id) VALUES ('{title}', '{category}', '{summary}', '{first_paragraph}', '{body}', '{author_id}') RETURNING paper_id, title, category, summary, first_paragraph, body, author_id'''
    result = engine.execute(query)
    created_paper = result.fetchone()
    return created_paper
