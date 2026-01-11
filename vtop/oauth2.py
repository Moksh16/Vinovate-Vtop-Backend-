from jose import JWTError,jwt
from datetime import datetime, timedelta,timezone
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ouath2scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=[ALGORITHM])
    return encoded_jwt


def verify_token(token:str, credential_exception):
    try:
        decoded__jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id :str = decoded__jwt.get("users.id")
        if id is None:
            raise credential_exception
        token_data =schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token:str = Depends(ouath2scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-authenticate": "Bearer"})
    return verify_token(token,credentials_exception)