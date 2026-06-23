from jose import JWTError, jwt

from datetime import datetime, timedelta, timezone

from app.db import database
from app.schemas import TokenData
from fastapi import Depends, HTTPException

# extracts token from req
from fastapi.security import OAuth2PasswordBearer
from app.db import models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "62bc94dd8c55da1738cfc40b8c32bffce6707d70ad5d680e7b42560cffa71380"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()    
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
                
        token_data = TokenData(id=int(id))

    except JWTError as e:
        print("JWT ERROR:", e)
        raise credentials_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=401, detail=f"Cant validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user
