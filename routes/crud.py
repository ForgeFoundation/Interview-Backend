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
openai_api_key = os.getenv("OPENAI_API_KEY2")


db = SessionLocal()

router = APIRouter(
    prefix="/crud",
    responses={404: {"description": "Not found"}},
    tags=["Crud"]
)


@router.get("/", status_code=200)
async def root():
    return {"message": "Crud API for SBU management."}



@router.post("/sign_user", status_code=201)
def sign_user( user: models.CreateUser):
    """Creates the user in the database if it does not exist. If it exists, it will update the last active time."""

    # Rollback 
    db.rollback()
    db_user = db.query(models.User).filter(models.User.firebaseid == user.firebaseid).first()
    if db_user:
        db_user.last_active = datetime.now()
        db.commit()
        db.refresh(db_user)
        return db_user

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
def get_prompts(collection_id: int = Query(None)):
    if collection_id:
        return db.query(models.Prompt).filter(models.Prompt.collection_id == collection_id).all()
    else:
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

    print("storing the following", promptid, answer.answer, answer.user_fid, answer.prompt_message, answer.is_public)
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
        user_name=user.username,
        timestamp=answer.timestamp
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
    
class SchemaPrevAnswers(models.BaseModel):
    user_fid: str
    prompt_message: str

@router.post(("/prev_answers"), status_code=200)
def get_prev_answers(prev_answers: SchemaPrevAnswers):
    """
    Retrieves previous answers from the user based on the prompt message.
    """
    
    print('called with', prev_answers.dict())
    answers = db.query(models.Answer).filter(
        models.Answer.user_fid == prev_answers.user_fid
    ).filter(
        models.Answer.prompt_message == prev_answers.prompt_message
    ).all()
    print(answers)
    

    return answers_to_answers_view(answers)



# Collections

@router.post("/collection", status_code=201)
def create_collection( collection: models.CreateCollection):
    
    db_collection = models.Collections(
        label = collection.label,
        description = collection.description
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection



@router.post('/generate_questions', status_code=201)
def generate_questions(generate_interview: models.question_generation_input):
    
    """
    Generate a new different interview question based on this type of job.
    """
    print(generate_interview.dict())
    openai.api_key = openai_api_key
    question = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an interviewer question maker"
            },
            {
                "role": "user",
                "content": "I am looking for a " + generate_interview.job_title + " position. Can you provide me with a question? "
            }
        ],        
        max_tokens=100
    )

    # Add the job title to the question bank


    response = question.choices[0].message.content
    return response



# @app.route("/generate_feedback", methods=["POST", "GET"])
# def generate_feedback():
#     data = request.json
#     # question
#     question = data["question"]
#     # answer
#     answer = data["answer"]
#     # feedback
#     feedback = openai.Completion.create(
#         model="gpt-3.5-turbo",
#         prompt="You are a coach. Give a feedback based on this " + question + " and this answer: " + answer,
#         max_tokens=1000
#     )


@router.post('/generate_feedback', status_code=201)
def generate_feedback(create_answer: models.CreateAnswer):
    """
    Generate feedback based on the question and the answer.
    """

    print(create_answer.dict())
    openai.api_key = openai_api_key
    feedback = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": "You are an interview coach. I provide me professional feedback for how I respond to the following question: " + create_answer.prompt_message 
        },
        {
            "role": "user",
            "content": create_answer.answer
        }
    ],
    max_tokens=100  # Limit the response to 100 tokens
    )
    response = feedback.choices[0].message.content
    return {"response": response}

# Profile Report

@router.get('/recent_answers', status_code=200)
def recent_answers(user_fid: str, limit: int = 20):
    """
    Retrieves the recent answers from the user.

    
        query = text(
            
            SELECT a.prompt_message, a.timestamp
            FROM (
                SELECT prompt_message, MAX(timestamp) AS timestamp
                FROM answers
                WHERE user_fid = :user_fid
                GROUP BY prompt_message
            ) AS latest_answers
            INNER JOIN answers AS a
            ON latest_answers.prompt_message = a.prompt_message
            AND latest_answers.timestamp = a.timestamp;
            
        )

        answers = db.execute(query, {'user_fid': user_fid}).all()
        print('====================')
    """
    try:
        answers = db.query(models.Answer).filter(
            models.Answer.user_fid == user_fid
        ).order_by(models.Answer.timestamp.desc()).limit(limit).all()

        unique_answers = {} # prompt: timestamp
        if not answers:
            return []
        for answer in answers:
            if answer.prompt_message not in unique_answers:
                unique_answers[answer.prompt_message] = answer.timestamp

        unique_answers_list = []
        for key, value in unique_answers.items():
            unique_answers_list.append({"prompt_message": key, "timestamp": value})

        return unique_answers_list
    except Exception as e:
        print(e)
        return []

@router.get('/heatmap_activity', status_code=200)
def heatmap_activity(user_fid: str):
    """
    Retrieves the heatmap activity from the user. n the format of:
    { date: '2024-01-01', count: 12 },
    { date: '2024-01-22', count: 122 },
    { date: '2024-01-30', count: 38 },
    {
        date: '2024-02-11',
        count: 12
    },
    {
        date: '2024-02-12',
        count: 1
    }

    Using saved responses.
    """
    answers = db.query(models.Answer).filter(
        models.Answer.user_fid == user_fid
    ).all()

    if not answers or len(answers) == 0:
        return []
    
    
    # Convert to the format of the heatmap.
    res_dict = {} # { date: '2024-01-01', count: 12 }
    for answer in answers:
        
        date_string = answer.timestamp.strftime("%Y-%m-%d")
        if date_string in res_dict:
            res_dict[date_string] += 1
        else:
            res_dict[date_string] = 1
    res_list = []
    for key, value in res_dict.items():
        res_list.append({"date": key, "count": value})

    return res_list


# Favorite an answer. Answers have to be unique among their prompt_message and user_fid.
@router.post('/toggle', status_code=201)
def favorite_answer(favorite: models.FavoriteAnswer):
    """
    Favorite an answer.
    """
    db_answer = db.query(models.Answer).filter(
        models.Answer.id == favorite.answer_id,
        models.Answer.user_fid == favorite.user_fid
    ).first()
    if not db_answer:
        return {"message": "Answer not found"}
    db_answer.is_favorite = not db_answer.is_favorite
    db.commit()
    db.refresh(db_answer)

    # Also turn off all others favorites if this is favorite

    if db_answer.is_favorite:
        db.query(models.Answer).filter(
            models.Answer.prompt_message == db_answer.prompt_message,
            models.Answer.user_fid == db_answer.user_fid
        ).filter(models.Answer.id != db_answer.id).update({models.Answer.is_favorite: False})
        db.commit()
    return db_answer

# Bookmarking a prompt
@router.post('/bookmark', status_code=201)
def bookmark(bookmark: models.CreateBookmarkPrompt):
    """
    Bookmark a prompt.
    
    """
    db_bookmark = models.BookmarkPrompt(user_fid=bookmark.user_fid, prompt_message=bookmark.prompt_message,
                                        timestamp=datetime.now())
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark



@router.get("/bookmarks", status_code=200)
def user_bookmarks(user_fid: str):
    """
    Retrieves the bookmarks from the user.
    Returns a list of bookmarks ['bookmark1']
    """
    bookmarks = db.query(models.BookmarkPrompt).filter(
        models.BookmarkPrompt.user_fid == user_fid
    ).all()
    bookmarks = set([bookmark.prompt_message for bookmark in bookmarks])
    print('fetching bookmarks', bookmarks)
    print(bookmarks)
    return list(bookmarks)


