from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Users
from ..utils import verify_password
from ..auth_jwt import create_access_token
from ..schemas import TokenData

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=TokenData)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # check if user exists in database
    user_query = db.query(Users).filter(Users.email == user_credentials.username)
    
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    # check if user password matches the one provided
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    payload = {'id': user.id}
    
    return {'access_token': create_access_token(payload), 'token_type': 'Bearer'}
