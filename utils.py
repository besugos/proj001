from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

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
    return token


def verify_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')
