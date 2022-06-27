
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, FastAPI, HTTPException, status

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

pwd_context = CryptContext(schemes=['bcrypt'])
SECRET_KEY = '1f23ab2c0cf6a0f3af6c320c9f1962adb112c3f1492a747b0adf740a41ee2b57'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_hash(plain_password):
    return pwd_context.hash(plain_password)


def verify_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict):
    local_data = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    local_data.update({'exp': expiry})
    token = jwt.encode(local_data, SECRET_KEY, algorithm=ALGORITHM)
    return {'token': token, 'exp': expiry}


def verify_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')


def get_token_expiry(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        return {'Error': str(e)}
    expiry = payload.get('exp')
    human_exp = datetime.fromtimestamp(expiry)
    now = datetime.now()
    if human_exp > now:
        return human_exp.strftime("%d/%m/%Y %H:%M")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired Token')
