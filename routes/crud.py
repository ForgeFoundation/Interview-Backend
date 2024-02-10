
from ast import List
from fastapi import APIRouter, Query
from datetime import datetime
from sqlalchemy import func, or_
import random
import models
from database import SessionLocal

db = SessionLocal()

router = APIRouter(
    prefix="/crud",
    responses={404: {"description": "Not found"}},
    tags=["Crud"]
)


@router.get("/", status_code=200)
async def root():
    return {"message": "Crud API for SBU management."}



@router.post("/create_user", status_code=201)
def create_user( user: models.CreateUser):
    db_user = models.User(firebaseid=user.firebaseid, username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




# Question Prompting

@router.post("/prompt", status_code=201)
def create_prompt( prompt: models.CreatePrompt):
    db_prompt = models.Prompt(prompt=prompt.prompt, tags=prompt.tags, description=prompt.description, hint=prompt.hint)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.get(("/prompt_random"), status_code=200)
def random_prompt(collection_id: int = Query(None), tag: str = Query(None)):
    """
    Retrieves a random prompt from the database. If collection_id is passed, it will retrieve a random prompt from the collection.
    If the tag: str is passed, it will retrieve a random prompt that has included such tag.
    """
    query = db.query(models.Prompt).order_by(func.random())
    if collection_id:
        query = query.filter(models.Prompt.collection_id == collection_id)
    if tag:
        query = query.filter(or_(models.Prompt.tags.contains([tag]), models.Prompt.tags == [tag]))

    # Randomize
    query = query.order_by(func.random())
    return query.first()


@router.get(("/prompt"), status_code=200)
def get_prompt(prompt_id: int):
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()

@router.get(("/prompts"), status_code=200)
def get_prompts():
    return db.query(models.Prompt).all()



# Answering Questions

@router.post('/answer', status_code=201)
def create_answer( answer: models.CreateAnswer):
    """
    Create an answer for a prompt.
    user_fid means the user's firebase id.
    """
    # Find if hte prompt_message exists, create a prompt if not.

    prompt_found = db.query(models.Prompt).filter(models.Prompt.prompt == answer.prompt_message).first()
    prompt_id = None
    if not prompt_found:
        prompt = models.Prompt(prompt=answer.prompt_message)
        db.add(prompt)
        db.commit()
        db.refresh(prompt)
        promptid = prompt.id
    else:
        promptid = prompt_found.id

    db_answer = models.Answer(
        answer=answer.answer,
        user_fid=answer.user_fid,
        
        prompt_message=answer.prompt_message,
        promptid=promptid,
        is_public=answer.is_public,

    )


    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.get(("/answer_public_by_prompt_id"), status_code=200)
def get_answer(prompt_id: int):
    """
    Retrieves answers based on the prompt id. Returns in the format of a list of the responses that were public.

    """
    answers = db.query(models.Answer).filter(
        models.Answer.promptid == prompt_id,
        models.Answer.is_public == True
    ).all()

    return answers





