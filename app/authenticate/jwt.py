from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("jwt_secret_key")

ALGORITHM = "HS256" 

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")