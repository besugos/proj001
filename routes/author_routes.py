from fastapi import HTTPException, status, Depends, Request

from models.models import Author

from fastapi import APIRouter

from slowapi import Limiter
from slowapi.util import get_remote_address

from persistency.author_persistency import read_authors, create_author, update_author
from persistency.persistency_utils import get_user_info

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])

router = APIRouter(
    prefix="/author",
    tags=["Author"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@limiter.limit("5/minute")
async def get_authors(request: Request, name: str = None, user=Depends(get_user_info)):
    authors = read_authors(name)
    return authors


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def create_authors(request: Request, author: Author, user=Depends(get_user_info)):
    if 'type' in user:
        if user['type'] == 'admin':
            created_author = create_author(author.name, author.picture)
            return created_author
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')


@router.patch("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1/minute")
async def update_authors(request: Request, author_id: int, author: Author, user=Depends(get_user_info)):
    if 'type' in user:
        if user['type'] == 'admin':
            result = update_author(author_id, author.name, author.picture)
            return result
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
