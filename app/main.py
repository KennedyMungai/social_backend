"""The entrypoint for the backend"""

import os
from time import sleep
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from pymysql import connect
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .models import Post as _Post

models.Base.metadata.create_all(bind=engine)

ENV = load_dotenv(find_dotenv())

app = FastAPI()

# Dependency


while True:
    try:
        conn = connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            db=os.environ.get("MYSQL_DATABASE")
        )

        print("Database connection successful")
        break

    except Exception as error:
        print(f"Connecting to the database failed. Has error: {error}")
        sleep(2)


cursor = conn.cursor()


class Post(BaseModel):
    """Created the Post class

    Args:
        BaseModel (Class): The parent class of Post
    """
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int] = None


@app.get("/")
async def root(_db: Session = Depends(get_db)) -> dict:
    """The root api endpoint

    Returns:
        dict: A message to show successful execution
    """
    _posts = _db.query(_Post).all()

    return {"data": _posts}


@app.get("/posts")
async def retrieve_all_posts(_db: Session = Depends(get_db)) -> dict:
    """An api endpoint to retrieve all posts

    Returns:
        dict: A dictionary containing the my_posts array
    """
    _posts = _db.query(_Post).all()
    return {"posts": _posts}


@app.get("/posts/{_id}")
async def retrieve_one_post(_id: int, _db: Session = Depends(get_db)):
    """An endpoint to retrieve a specified post

    Args:
        _id (int): The id of the post

    Returns:
        dict: Outputs the post data
    """
    _post = _db.query(Post).filter(_Post.id == _id).first()
    _db.commit()
    _db.refresh(_post)

    return {"data": _post}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_post(_new_post: Post, _db: Session = Depends(get_db)) -> dict:
    """The create post endpoint

    Args:
        _post (Post): The post

    Returns:
        dict: A returned dictionary to show successful execution of the logic
    """
    _post = _Post(**_new_post.dict())

    _db.add(_post)
    _db.commit()
    _db.refresh(_post)

    return {"data": _post}


@app.delete("/posts/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_post(_id: int, _db: Session = Depends(get_db)):
    """An endpoint for deleting posts

    Args:
        _id (int): The id of the post

    Raises:
        HTTPException: A not found exception is raised if the post is not found in my_posts

    Returns:
        dict: A message to show the successful execution of the code
    """
    _post = _db.query(_Post).filter(_Post.id == _id)

    if not _post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id: {_id} could be found"
        )

    _post.delete(synchronize_session=False)
    _db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{_id}")
async def update_post(_id: int, _new_post: Post, _db: Session = Depends(get_db)) -> dict:
    """Created the update endpoint

    Args:
        _id (int): The id of the post
        _new_post (Post): The data to update the post

    Raises:
        HTTPException: A not found exception is raised when the post is not found

    Returns:
        dict: A message is shown when the logic is successfully run
    """
    _post_query = _db.query(_Post).filter(_Post.id == id)

    _post = _post_query.first()

    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post of id: {_id} was not found"
        )

    _post_query.update(_post.dict(), synchronize_session=False)

    _db.commit()

    return {"post": _post_query.first()}
