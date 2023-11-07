import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.configs.environment import get_config

config = get_config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             config.JWT_SECRET,
                             algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    return jwt.decode(token,
                      config.JWT_SECRET,
                      algorithms=[config.JWT_ALGORITHM])
