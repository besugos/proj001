import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



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


def read_users():
    session = get_session()
    query = 'SELECT * FROM proj001.user'
    cursor = session.execute(query).cursor
    users = rows_as_dicts(cursor)
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


def read_authors(name: str = None):
    session = get_session()
    query = 'SELECT * FROM proj001.author'
    if name is not None:
        query = query + f" WHERE LOWER(name) LIKE LOWER('%{name}%')"
    cursor = session.execute(query).cursor
    authors = rows_as_dicts(cursor)
    return authors


def create_author(name: str, picture: str):
    engine = get_engine()
    query = f'''INSERT INTO proj001.author (name, picture) VALUES ('{name}', '{picture}') RETURNING author_id, name, picture'''
    result = engine.execute(query)
    created_author = result.fetchone()
    return created_author


def read_papers(name: str = None):
    session = get_session()
    query = 'SELECT * FROM proj001.paper'
    if name is not None:
        query = query + f" WHERE LOWER(name) LIKE LOWER('%{name}%')"
    cursor = session.execute(query).cursor
    papers = rows_as_dicts(cursor)
    return papers

