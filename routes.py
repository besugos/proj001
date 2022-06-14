from fastapi import FastAPI

from models import Author
from persistency import read_users, read_authors, read_papers, create_author

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


@app.get("/authors")
async def get_authors(name: str = None):
    authors = read_authors(name)
    return authors


@app.post("/authors")
async def post_authors(author: Author):
    created_author = create_author(author.name, author.picture)
    return created_author


@app.get("/papers")
async def get_papers():
    papers = read_papers()
    return papers