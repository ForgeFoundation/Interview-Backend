from typing import List
from fastapi import APIRouter, Query
from datetime import datetime
import openai
from sqlalchemy import func, or_
import random
import models
from database import SessionLocal

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
openai_api_key = os.getenv("OPENAI_API_KEY")


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

def answer_to_answer_view(answer: models.Answer):
    user = db.query(models.User).filter(models.User.firebaseid == answer.user_fid).first()
    return models.ViewAnswer(
        answer=answer.answer,
        promptid=answer.promptid,
        prompt_message=answer.prompt_message,
        user_fid=answer.user_fid,
        user_name=user.username
    )

def answers_to_answers_view(answers: List[models.Answer]):
    return [answer_to_answer_view(answer) for answer in answers]

@router.get(("/answer_public_by_prompt_id"), status_code=200)
def get_answer(prompt_id: int):
    """
    Retrieves answers based on the prompt id. Returns in the format of a list of the responses that were public.

    """
    answers = db.query(models.Answer).filter(
        models.Answer.promptid == prompt_id,
        models.Answer.is_public == True
    ).all()
    return answers_to_answers_view(answers)
    

@router.get(("/prev_answers"), status_code=200)
def get_prev_answers(user_fid: str, prompt_message: str):
    """
    Retrieves previous answers from the user based on the prompt message.
    """
    answers = db.query(models.Answer).filter(
        models.Answer.user_fid == user_fid,
        models.Answer.prompt_message == prompt_message
    ).all()

    return answers_to_answers_view(answers)



# Collections

@router.post("/collection", status_code=201)
def create_collection( collection: models.CreateCollection):
    
    db_collection = models.Collection(name=collection.name, description=collection.description)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection



@router.post('/generate_questions', status_code=201)
def generate_questions(generate_interview: models.question_generation_input):
    
    """
    Generate a new different interview question based on this type of job.
    """
    openai.api_key = openai_api_key
    completion = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="generate a new different interview question based on this type of job: " + str(generate_interview.dict()),
        max_tokens=1000
    )

    return {"response": completion.choices[0].text.strip()}



# @app.route("/generate_feedback", methods=["POST", "GET"])
# def generate_feedback():
#     data = request.json
#     # question
#     question = data["question"]
#     # answer
#     answer = data["answer"]
#     # feedback
#     feedback = openai.Completion.create(
#         model="gpt-3.5-turbo-instruct",
#         prompt="You are a coach. Give a feedback based on this " + question + " and this answer: " + answer,
#         max_tokens=1000
#     )


@router.post('/generate_feedback', status_code=201)
def generate_feedback(create_answer: models.CreateAnswer):
    """
    Generate feedback based on the question and the answer.
    """
    openai.api_key = openai_api_key
    feedback = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="You are a coach. Give a feedback based on this " + create_answer.prompt_message + " and this answer: " + create_answer.answer,
        max_tokens=1000
    )
    return {"response": feedback.choices[0].text.strip()}


