from  datetime import datetime

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .database import SessionLocal
from .models import Tasks


MINIMUM_PASSWORD_LENGTH = 8
SYMBOLS = [
    ' ', '~', '`', '!', '@', '#', '$', '%', 
    '^', '&', '*', '(', ')', '_', '-', '+', 
    '=', '{', '[', '}', ']', '|', ':', ';', 
    '<', ',', '>', '.', '/'
]

passlib_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# hash password provided by user
def hash_password(password_to_hash: str) -> str:
    '''hashes the password provided by user'''
    return passlib_context.hash(password_to_hash)


# verify if attempted password matches db_password
def verify_password(attempted_password: str, db_password: str) -> bool:
    '''verify password provided by user is the same as on in database'''
    return passlib_context.verify(attempted_password, db_password)


# check password length
def password_lt_minimum(password: str) -> bool:
    '''checks if password length is less than minimum length'''
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return True
    return False


# check if password contains an uppercase, a symbol and a number
def password_meets_requirements(password: str) -> bool:
    '''checks if password meets requirements'''
    uppercase_check = integer_check = symbol_check = False
    
    for char in password:
        if ord(char) in range(65, 91):
            uppercase_check = True
        if char.isdigit():
            integer_check = int(char) in range(0, 10)
        if char in SYMBOLS:
            symbol_check = True
    
    # check if all requirements are met
    if all([uppercase_check, integer_check, symbol_check]):
        return True
    return False


# set all tasks that are outdated is_active to False
def set_all_inactive_tasks_to_false():
    '''set all inactive tasks to false'''
    db = SessionLocal()
    tasks = db.query(Tasks).all()
    if len(tasks) > 0:
        for task in tasks:
            if task.time_due < datetime.utcnow():
                db.query(Tasks).filter(Tasks.id == task.id).update({'is_active': False})
                db.commit()
            else:
                db.query(Tasks).filter(Tasks.id == task.id).update({'is_active': True})
                db.commit()
    db.close()
