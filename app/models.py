from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship

from .database import Base

# users model
class Users(Base):
    __tablename__ = 'users'
    
    id = Column('id', Integer, primary_key=True, nullable=False)
    email = Column('email', String(255), nullable=False, unique=True)
    password = Column('password', String(255), nullable=False)
    username = Column('username', String(255), nullable=False, unique=True)
    created_at = Column('created_at', TIMESTAMP(timezone=True), server_default=expression.text('NOW()'), nullable=False)


# task model
class Tasks(Base):
    __tablename__ = 'tasks'
    
    id = Column('id', Integer, primary_key=True, nullable=False)
    task = Column('task', String(255), nullable=False)
    time_due = Column('time_due', TIMESTAMP(timezone=True), nullable=False)
    remind_me = Column('reminder', Boolean, server_default=expression.false(), nullable=False)
    repeat = Column('repeat', Boolean, server_default=expression.false(), nullable=False)
    is_active = Column('is_active', Boolean, server_default=expression.false(), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column('created_at', TIMESTAMP(timezone=True), server_default=expression.text('NOW()'), nullable=False)
    
    user = relationship('Users')
