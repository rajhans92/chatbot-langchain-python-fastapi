import jwt
from datetime import datetime, timedelta
from app.helpers.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_TIME_HOURS

def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode['exp'] = datetime.utcnow() + timedelta(hours=JWT_TOKEN_TIME_HOURS)
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")