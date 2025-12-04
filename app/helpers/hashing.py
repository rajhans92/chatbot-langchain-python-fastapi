from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    hashed_password = pwd_context.hash(password)
    print(hashed_password)
    return hashed_password

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
