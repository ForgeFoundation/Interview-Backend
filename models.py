
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
    firebaseid = Column(String, nullable=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=False)
    last_active = Column(DateTime, default=func.now(), nullable=False)


class CreateUser(BaseModel):
    firebaseid: str
    username: str
    email: str
    class Config:
        orm_mode = True

class ViewUser(BaseModel):   
    id: int
    firebaseid: str
    username: str
    email: str
    last_active: datetime.datetime
    class Config:
        orm_mode = True


class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    description = Column(String, nullable=True)
    hint = Column(String, nullable=True)
    collection_id = Column(Integer, nullable=True)

class CreatePrompt(BaseModel):

    prompt: str
    tags: List[str]
    description: str
    hint: str

    class Config:
        orm_mode = True

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(String, nullable=False)

    prompt_message = Column(String, nullable=False) # It could be assigned to an non idead prompt.
    promptid = Column(Integer, nullable=True)
    user_fid = Column(String, nullable=True)
    is_public = Column(Boolean, nullable=True, default=False)    
    
    # After iterations
    votes = Column(Integer, nullable=False, default=0)
    how_confident = Column(Integer, nullable=True)
    last_feedback_id = Column(Integer, nullable=True)

    timestamp = Column(DateTime, default=func.now(), nullable=False)


class ViewAnswer(BaseModel):
    answer: str
    promptid: int
    prompt_message: str
    user_fid: str
    user_name: str


class CreateAnswer(BaseModel):
    """
    Just for creating asnwer with no grading yet.
    """
    answer: str
    user_fid: str

    prompt_message: str
    is_public: bool
    class Config:
        orm_mode = True


class Collections(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    tags = Column(ARRAY(String), nullable=True)

class CreateCollection(BaseModel):
    label: str
    description: str
    image: str
    tags: List[str]
    class Config:
        orm_mode = True

class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)\
    

    
# Expected schema
class question_generation_input(BaseModel):
    job_title: str
    job_type: str
    job_description: str
    industry: str
    location: str

    class Config:
        orm_mode = True
