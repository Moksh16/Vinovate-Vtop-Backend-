from passlib.context import CryptContext
password_hasher = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password:str):
    return password_hasher.hash(password)

def verify_password(original_password, hashed_password):
    return password_hasher.verify(original_password, hashed_password)