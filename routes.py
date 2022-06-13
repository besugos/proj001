from fastapi import FastAPI

from persistency import read_users, read_authors, read_papers

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


@app.get("/papers")
async def get_papers():
    papers = read_papers()
    return papers