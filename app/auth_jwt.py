from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .config import settings
from .schemas import TokenPayload
from .database import get_db
from .models import Users

TOKEN_URL = '/login'

oauth_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

def create_access_token(payload: dict):
    '''create access token anytime client logs in'''
    payload_to_decode = payload.copy()
    
    expires = datetime.utcnow() + timedelta(minutes=settings.access_token_minute_expires)
    
    payload_to_decode.update({'exp': expires})
    
    token = jwt.encode(payload_to_decode, settings.secret_key, algorithm=settings.algorithm)
    
    print(oauth_scheme)
    
    return token


def verify_access_token(token: str, credentials_exception: Exception):
    '''verify access token provided by client'''
    try:
        decoded_token = jwt.decode(token, settings.secret_key, settings.algorithm)
        
        id: str = decoded_token['id']
        expires: datetime = decoded_token['exp']
        
        # raise exception if id is none
        if id is None:
            raise credentials_exception
        
        # raise exception if token has expired
        if datetime.utcfromtimestamp(expires) < datetime.utcnow():
            raise credentials_exception

        token_data = TokenPayload(id=id, exp=expires)
        
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f'Invalid credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    
    user_query = db.query(Users).filter(Users.id == token_data.id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    return user
