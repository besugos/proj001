from fastapi import APIRouter, Request, Depends, status, HTTPException

from src.models.models import Paper
from src.persistency.author_persistency import read_author_by_id
from src.persistency.paper_persistency import read_papers, create_paper, update_paper

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.persistency.persistency_utils import get_user_info

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])

router = APIRouter(
    prefix="/paper",
    tags=["Paper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@limiter.limit("10/minute")
async def get_papers(request: Request, title: str = None, user=Depends(get_user_info)):
    papers = read_papers(title)
    for paper in papers:
        paper['author'] = read_author_by_id(paper['author_id'])
        paper.pop('author_id')
    return papers


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def create_authors(request: Request, paper: Paper, user=Depends(get_user_info)):
    if 'type' in user:
        if user['type'] == 'admin':
            created_paper = create_paper(paper.title, paper.category, paper.summary, paper.first_paragraph, paper.body, paper.author_id)
            return created_paper
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')



@router.patch("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1/minute")
async def update_papers(request: Request, paper_id: int, paper: Paper, user=Depends(get_user_info)):
    if 'type' in user:
        if user['type'] == 'admin':
            result = update_paper(paper_id, paper.title, paper.category, paper.summary, paper.first_paragraph, paper.body, paper.author_id)
            return result
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
