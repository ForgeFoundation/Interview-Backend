
from fastapi import APIRouter, Query
from datetime import datetime
from sqlalchemy import or_, and_
from database import SessionLocal
from typing import Optional
import models

db = SessionLocal()


router = APIRouter(
    prefix="/forum",
    responses={404: {"description": "Not found"}},
    tags=["Forum"]
)


@router.post("/get_create_user", status_code=200)
def getOrCreateUser(email:str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user
    else:
        new_user = models.User(
            email=email,
            last_active=datetime.now()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get("/", status_code=200)
async def getForums(string_filter: Optional[str] = Query(None)):
    print("String filter", string_filter)
    if string_filter == "" or string_filter == None:
        forums = db.query(models.Thread).all()
        return forums
    forums = db.query(models.Thread).filter(
        and_(
            or_(models.Thread.title.ilike(f"%{string_filter}%"), models.Thread.body.ilike(f"%{string_filter}%")),
            models.Thread.is_forum == True
        )
        ).all()
    return forums

@router.post('/', status_code=201)
def createForum(forum: models.CreateCommentWithEmail):

    user = getOrCreateUser(forum.email)

    new_forum = models.Thread(
        is_forum=True,
        title=forum.title,
        body=forum.body,
        user_id=user.id,
        created_time=datetime.now(),
        tags=[]
    )
    db.add(new_forum)
    db.commit()
    db.refresh(new_forum)
    return new_forum

@router.get("/{forum_id}", status_code=200)
def getForum(forum_id: int):
    """Returns the forum details and an array of comments recurively

    Args:
        forum_id (int): The id of the forum

    """
    def getCommentsOfParentId(parent_id, depth=0, max_depth=10):
        if depth >= max_depth:
            return []

        forum_data = {}
        comments_list = []

        forum = db.query(models.Thread).filter(models.Thread.thread_id == forum_id).first()
        if not forum:
            return forum_data  # Return empty data if the forum does not exist

        comments = db.query(models.Thread).filter(models.Thread.parent_id == parent_id).all()

        for comment in comments:
            # print(comment, comment.thread_id, comment.parent_id)
            # comment_data = getCommentsOfParentId(comment.thread_id, depth + 1, max_depth)
            # comments_list.append(comment_data)
            # forum = db.query(models.Thread).filter(models.Thread.thread_id == forum_id).first()
            # if not forum:
            #     return forum_data  # Return empty data if the forum does not exist

            comments = db.query(models.Thread).filter(models.Thread.parent_id == comment.thread_id).all()
            comments_list.append({"forum": comment, "comments": comments})

        forum_data["forum"] = forum
        forum_data["comments"] = comments_list

        return forum_data

    forum_data = getCommentsOfParentId(forum_id)
    return forum_data


@router.post("/comments", status_code=201)
def createComment(comment: models.CreateCommentWithEmail):
    """Creates a comment on a forum or thread

    Args:
        forum_id (int): The id of the forum or thread

    """

    user = getOrCreateUser(comment.email)

    new_comment = models.Thread(
        is_forum=False,
        body=comment.body,
        user_id=user.id,
        title=comment.title,
        parent_id=comment.parent_id,
        tags=[],
        created_time=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment





