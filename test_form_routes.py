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

def create_behavioural_collection():
    collection = models.CreateCollection(label="behavioural", description="This is a collection of behavioural interview questions")
    response = create_collection(collection)
    """
    What was the last project you headed up, and what was its outcome?
    Give me an example of a time that you felt you went above and beyond the call of duty at work.
    Can you describe a time when your work was criticized?
    Have you ever been on a team where someone was not pulling their own weight? How did you handle it?
    Tell me about a time when you had to give someone difficult feedback. How did you handle it?
    What is your greatest failure, and what did you learn from it?
    What irritates you about other people, and how do you deal with it?
    If I were your supervisor and asked you to do something that you disagreed with, what would you do?
    What was the most difficult period in your life, and how did you deal with it?
    Give me an example of a time you did something wrong. How did you handle it?
    What irritates you about other people, and how do you deal with it?
    Tell me about a time where you had to deal with conflict on the job.
    If you were at a business lunch and you ordered a rare steak and they brought it to you well done, what would you do?
    If you found out your company was doing something against the law, like fraud, what would you do?
    What assignment was too difficult for you, and how did you resolve the issue?
    What's the most difficult decision you've made in the last two years and how did you come to that decision?
    Describe how you would handle a situation if you were required to finish multiple tasks by the end of the day, and there was no conceivable way that you could finish them.
    """

    promptsLists = [
        CreatePrompt(prompt="What was the last project you headed up, and what was its outcome?", tags=["behavioural-interview"], description="This is a question about the last project you headed up", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Give me an example of a time that you felt you went above and beyond the call of duty at work.", tags=["behavioural-interview"], description="This is a question about a time that you felt you went above and beyond the call of duty at work", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Can you describe a time when your work was criticized?", tags=["behavioural-interview"], description="This is a question about a time when your work was criticized", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Have you ever been on a team where someone was not pulling their own weight? How did you handle it?", tags=["behavioural-interview"], description="This is a question about a time when someone was not pulling their own weight", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Tell me about a time when you had to give someone difficult feedback. How did you handle it?", tags=["behavioural-interview"], description="This is a question about a time when you had to give someone difficult feedback", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="What is your greatest failure, and what did you learn from it?", tags=["behavioural-interview"], description="This is a question about your greatest failure", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="What irritates you about other people, and how do you deal with it?", tags=["behavioural-interview"], description="This is a question about what irritates you about other people", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="If I were your supervisor and asked you to do something that you disagreed with, what would you do?", tags=["behavioural-interview"], description="This is a question about if I were your supervisor and asked you to do something that you disagreed with", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="What was the most difficult period in your life, and how did you deal with it?", tags=["behavioural-interview"], description="This is a question about the most difficult period in your life", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Give me an example of a time you did something wrong. How did you handle it?", tags=["behavioural-interview"], description="This is a question about a time you did something wrong", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="What irritates you about other people, and how do you deal with it?", tags=["behavioural-interview"], description="This is a question about what irritates you about other people", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Tell me about a time where you had to deal with conflict on the job.", tags=["behavioural-interview"], description="This is a question about a time where you had to deal with conflict on the job", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="If you were at a business lunch and you ordered a rare steak and they brought it to you well done, what would you do?", tags=["behavioural-interview"], description="This is a question about a business lunch", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="If you found out your company was doing something against the law, like fraud, what would you do?", tags=["behavioural-interview"], description="This is a question about your company doing something against the law", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="What assignment was too difficult for you, and how did you resolve the issue?", tags=["behavioural-interview"], description="This is a question about an assignment that was too difficult for you", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="What's the most difficult decision you've made in the last two years and how did you come to that decision?", tags=["behavioural-interview"], description="This is a question about the most difficult decision you've made in the last two years", hint="It is a question about your personal reasons", collection_id=response["id"]),
        CreatePrompt(prompt="Describe how you would handle a situation if you were required to finish multiple tasks by the end of the day, and there was no conceivable way that you could finish them.", tags=["behavioural-interview"], description="This is a question about how you would handle a situation if you were required to finish multiple tasks by the end of the day", hint="It is a question about your personal reasons", collection_id=response["id"])
    ]

    for prompt in promptsLists:
        createPrompts(prompt)


def test_create_prompts():
    # for prompt in promptsLists:
    #     createPrompts(prompt)

    fundamentals_collection = create_collection(models.CreateCollection(label="fundamentals", description="This is a collection of fundamental interview questions"))
    create_collection(fundamentals_collection)
    # create_behavioural_collection()




    
