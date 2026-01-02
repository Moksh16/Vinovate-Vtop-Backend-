from passlib.context import CryptContext
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    new_pwd = password_hasher.hash(password)
    return new_pwd