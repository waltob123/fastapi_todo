from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserCreateModel, UserResponseModel, UserUpdateModel
from ..utils import hash_password, password_lt_minimum, password_meets_requirements
from ..models import Users
from ..auth_jwt import get_current_user


# Router to users endpoint
router = APIRouter(prefix='/users', tags=['Users'])

# create new user
@router.post('/', status_code=status.HTTP_201_CREATED
, response_model=UserResponseModel)
def create_user(user: UserCreateModel, db: Session = Depends(get_db)):
    new_user = Users(**user.dict())
    
    # check if password is less than minimum
    if password_lt_minimum(new_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='uassword should be at least 8 characters long.')
    
    # check if password meets requirements
    if not password_meets_requirements(new_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='password should contain at lease 1 uppercase, integer and symbol')

    # hash password
    new_user.password = hash_password(new_user.password)
    
    # add new user
    db.add(new_user)
    
    # commit new user to database
    try:
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user exists already')
    
    db.refresh(new_user)
    
    return new_user


# delete user account
@router.delete('/')
def delete_user(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    user_query = db.query(Users).filter(Users.id == current_user.id)
    user = user_query.first()
    
    # check if user exists
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} not found')
    
    user_query.delete(synchronize_session=False)
    
    try:
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'user with id: {id} cannot be deleted')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update user account with username
@router.put('/', response_model=UserResponseModel)
def update_user(user: UserUpdateModel, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    user_query = db.query(Users).filter(Users.id == current_user.id)
    
    user_to_be_updated = user_query.first()
    
    if user_to_be_updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} not found')
    
    user_query.update(user.dict(), synchronize_session=False)
    
    try:
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'username exists already')
    return user_to_be_updated
