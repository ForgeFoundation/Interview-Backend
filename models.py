
from email.policy import default
from sqlalchemy import PrimaryKeyConstraint, String,Boolean,Integer,Column, Table,Text, DateTime, ARRAY, Identity, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import datetime, uuid
import shortuuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import func



import json
Base = declarative_base()

from pydantic import BaseModel
from typing import List, Optional



# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String, nullable=False, server_default=func.gen_random_uuid())
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    email = Column(String, nullable=False)
    tags = Column(ARRAY(String))
    languages = Column(ARRAY(String))
    last_active = Column(DateTime, default=func.now(), nullable=False)



class CreateUser(BaseModel):
    username: str
    email: str
    tags: List[str]
    languages: List[str]

    class Config:
        orm_mode = True

class ViewUser(BaseModel):
    id: int
    username: str
    email: str
    tags: List[str]
    languages: List[str]
    last_active: datetime.datetime

    class Config:
        orm_mode = True




# Define the Thread model
class Thread(Base):
    __tablename__ = 'threads'

    thread_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('threads.thread_id'), nullable=True)
    is_forum = Column(Boolean, nullable=False)
    guid = Column(String, nullable=False, server_default=func.gen_random_uuid())
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    tags = Column(ARRAY(String), nullable=False)



class CreateForum(BaseModel):
    title: str
    body: str
    user_id: int
    tags: List[str]


class CreateForumEmail(BaseModel):
    title: str
    body: str
    email: str


class CreateComment(BaseModel):
    body: str
    title: str
    user_id: int
    parent_id: int


class CreateCommentWithEmail(BaseModel):
    body: str
    title: str
    email: str
    parent_id: int


