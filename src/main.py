import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi import APIRouter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.routes import user_routes, author_routes, paper_routes

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


router = APIRouter()
router.include_router(user_routes.router)
router.include_router(author_routes.router)
router.include_router(paper_routes.router)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
    print("running")
