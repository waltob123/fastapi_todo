from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserCreateModel, UserResponseModel
from ..utils import hash_password, verify_password, password_lt_minimum, password_meets_requirements
from ..models import Users


# Router to users endpoint
router = APIRouter(prefix='/users', tags=['Users'])

# create new user
@router.post('/', status_code=status.HTTP_201_CREATED
, response_model=UserResponseModel)
def create_user(user: UserCreateModel, db: Session = Depends(get_db)):
    new_user = Users(**user.dict())
    
    # check if password is less than minimum
    if password_lt_minimum(new_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password should be at least 8 characters long.')
    
    # check if password meets requirements
    if not password_meets_requirements(new_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password should contain at lease 1 uppercase, integer and symbol')

    # hash password
    new_user.password = hash_password(new_user.password)
    
    # add new user
    db.add(new_user)
    
    # commit new user to database
    try:
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User exists already')
    
    db.refresh(new_user)
    
    return new_user
