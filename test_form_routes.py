from ast import List
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app

from models import CreateUser, CreatePrompt
import models


client = TestClient(app)



# Tell me about yourself.
# What are your strengths?
# What are your weaknesses?
# Why do you want this job?
# Where would you like to be in your career five years from now?
# What's your ideal company?
# What attracted you to this company?
# Why should we hire you?
# What did you like least about your last job?
# When were you most satisfied in your job?
# What can you do for us that other candidates can't?
# What were the responsibilities of your last position?
# Why are you leaving your present job?
# What do you know about this industry?
# What do you know about our company?
# Are you willing to relocate?
# Do you have any questions for me?

promptsLists = [
    CreatePrompt(prompt="Tell me about yourself.", tags=["core-interview"], description="This is a question about yourself", hint="It is a question about your personal life"),
    CreatePrompt(prompt="What are your strengths?", tags=["core-interview"], description="This is a question about your strengths", hint="It is a question about your personal strengths"),
    CreatePrompt(prompt="What are your weaknesses?", tags=["core-interview"], description="This is a question about your weaknesses", hint="It is a question about your personal weaknesses"),
    CreatePrompt(prompt="Why do you want this job?", tags=["core-interview"], description="This is a question about why you want this job", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="Where would you like to be in your career five years from now?", tags=["core-interview"], description="This is a question about your future", hint="It is a question about your future"),
    CreatePrompt(prompt="What's your ideal company?", tags=["core-interview"], description="This is a question about your ideal company", hint="It is a question about your ideal company"),
    CreatePrompt(prompt="What attracted you to this company?", tags=["core-interview"], description="This is a question about what attracted you to this company", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="Why should we hire you?", tags=["core-interview"], description="This is a question about why should we hire you", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="What did you like least about your last job?", tags=["core-interview"], description="This is a question about your last job", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="When were you most satisfied in your job?", tags=["core-interview"], description="This is a question about your satisfaction", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="What can you do for us that other candidates can't?", tags=["core-interview"], description="This is a question about what can you do for us", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="What were the responsibilities of your last position?", tags=["core-interview"], description="This is a question about your last position", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="Why are you leaving your present job?", tags=["core-interview"], description="This is a question about why are you leaving your present job", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="What do you know about this industry?", tags=["core-interview"], description="This is a question about what do you know about this industry", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="What do you know about our company?", tags=["core-interview"], description="This is a question about what do you know about our company", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="Are you willing to relocate?", tags=["core-interview"], description="This is a question about are you willing to relocate", hint="It is a question about your personal reasons"),
    CreatePrompt(prompt="Do you have any questions for me?", tags=["core-interview"], description="This is a question about do you have any questions for me", hint="It is a question about your personal reasons")
    
]
def createPrompts(prompt: CreatePrompt):
    response = client.post("/crud/prompt", json=prompt.dict())
    assert response.status_code == 201
    return response.json()

def create_collection (collection: models.CreateCollection):
    response = client.post("/crud/collection", json=collection.dict())
    assert response.status_code == 201
    return response.json()

def test_create_prompts():
    # for prompt in promptsLists:
    #     createPrompts(prompt)

    fundamentals_collection = create_collection(models.CreateCollection(name="fundamentals", description="This is a collection of fundamental interview questions"))
    
