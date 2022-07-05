from fastapi import HTTPException, status, Depends, Request

from fastapi.security import OAuth2PasswordBearer

from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.models.models import User, LoginData

from src.persistency.persistency_utils import get_user_info
from src.persistency.user_persistency import read_users, create_user, get_user_by_username
from src.utils.utils import create_hash, verify_hash, create_token, get_token_expiry


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@limiter.limit("5/minute")
async def get_users(request: Request, current_user=Depends(get_user_info)):
    users = read_users()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def post_user(request: Request, user: User, current_user: object = Depends(get_user_info)):
    if 'type' in current_user:
        if current_user['type'] == 'admin':
            password = create_hash(user.password)
            created_user = create_user(user.type, user.username, password)
            return created_user


@router.post("/token")
@limiter.limit("10/minute")
async def login(request: Request, login_data: LoginData):
    password = login_data.password
    username = login_data.username
    user = get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong credentials')

    # valid_password = verify_hash(password, user['password'])

    # if not valid_password:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong credentials')

    token = create_token({'sub': user['username'], 'aut': user['type']})

    return {"user": user, "token": token['token'], 'expires at': token['exp'].strftime("%d/%m/%Y %H:%M")}


@router.get("/me")
@limiter.limit("1/minute")
async def me(request: Request, user=Depends(get_user_info)):
    return user


@router.get("/expiry")
@limiter.limit("10/minute")
async def expiry(request: Request, exp=Depends(get_token_expiry)):
    if 'Error' in exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired Token')
    return {'Token expires at': exp}
