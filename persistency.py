from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/projeto001")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


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


def read_authors(name: str = None):
    session = get_session()
    query = 'SELECT * FROM proj001.author'
    if name is not None:
        query = query + f" WHERE LOWER(name) LIKE LOWER('%{name}%')"
    cursor = session.execute(query).cursor
    authors = rows_as_dicts(cursor)
    return authors


def read_papers():
    session = get_session()
    query = 'SELECT * FROM proj001.paper'
    cursor = session.execute(query).cursor
    papers = rows_as_dicts(cursor)
    return papers

