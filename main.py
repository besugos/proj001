# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Author
from persistency.persistency import rows_as_dicts

engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/projeto001")
Session = sessionmaker(bind=engine)
session = Session()

author = Author
author.name = 'Juca'
author.picture = 'teste'
author.author_id = 101

print(author)

query = f'''INSERT INTO proj001.author VALUES (10, '{author['name']}', '{author['picture']}')'''
# query = f'''INSERT 11, "Zé", "teste" INTO
try:
    session.execute(query)
    session.commit()
except Exception as e:
    raise e
# authors = rows_as_dicts(cursor)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def test_db():
    # result = session.execute('SELECT * FROM proj001.author')
    # for row in result:
    #     print(row)
    query = 'SELECT * FROM proj001.author'
    cursor = session.execute(query).cursor
    authors = rows_as_dicts(cursor)
    print(authors)


test_db()
