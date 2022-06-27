from fastapi import APIRouter

from persistency.paper_persistency import read_papers

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])

router = APIRouter(
    prefix="/paper",
    tags=["Paper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@limiter.limit("5/minute")
async def get_papers():
    papers = read_papers()
    return papers
