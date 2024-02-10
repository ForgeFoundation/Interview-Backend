
from ast import List
from fastapi import APIRouter, Query
from datetime import datetime
from sqlalchemy import func, or_
import random
import models
from database import SessionLocal
import openai


db = SessionLocal()


router = APIRouter(
    prefix="/crud",
    responses={404: {"description": "Not found"}},
    tags=["Crud"]
)

class JobPrompt(BaseModel):
    job_title: str
    job_type: str
    job_description: str
    industry: str
    location: str

@app.post("/generate_questions")
async def generate_questions(prompt: JobPrompt):
    completion = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="generate a new different interview question based on this type of job: " + str(prompt.dict()),
        max_tokens=1000
    )

    return {"response": completion.choices[0].text.strip()}

class FeedbackInput(BaseModel):
    question: str
    answer: str

@app.post("/generate_feedback")
async def generate_feedback(data: FeedbackInput):
    feedback = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="You are a coach. Give a feedback based on this " + data.question + " and this answer: " + data.answer,
        max_tokens=1000
    )

    return {"response": feedback.choices[0].text.strip()}