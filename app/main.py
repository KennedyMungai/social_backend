"""The entrypoint for the backend"""

import os
from time import sleep
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from pymysql import connect

from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

ENV = load_dotenv(find_dotenv())

app = FastAPI()

# Dependency


def get_db():
    """The database dependency

    Yields:
        Session: The database session
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


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
async def root() -> dict:
    """The root api endpoint

    Returns:
        dict: A message to show successful execution
    """
    return {"Message": "Hello World"}


@app.get("/posts")
async def retrieve_all_posts() -> dict:
    """An api endpoint to retrieve all posts

    Returns:
        dict: A dictionary containing the my_posts array
    """
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"posts": posts}


@app.get("/posts/{_id}")
async def retrieve_one_post(_id: int):
    """An endpoint to retrieve a specified post

    Args:
        _id (int): The id of the post

    Returns:
        dict: Outputs the post data
    """
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (_id))

    _post = cursor.fetchone()

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {_id} was not found")

    return _post


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_post(_new_post: Post) -> dict:
    """The create post endpoint

    Args:
        _post (Post): The post

    Returns:
        dict: A returned dictionary to show successful execution of the logic
    """
    cursor.execute(
        """INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)""", (
            _new_post.title, _new_post.content, _new_post.published)
    )

    _new_post = cursor.fetchone()

    conn.commit()

    return {"data": _new_post}


@app.delete("/posts/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_post(_id: int):
    """An endpoint for deleting posts

    Args:
        _id (int): The id of the post

    Raises:
        HTTPException: A not found exception is raised if the post is not found in my_posts

    Returns:
        dict: A message to show the successful execution of the code
    """
    _post = cursor.execute("""SELECT * FROM posts WHERE id = %s""", (_id))

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with the id of {_id} was not found")

    cursor.execute("""DELETE FROM posts WHERE id = %s""", (_id))

    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{_id}")
async def update_post(_id: int, _new_post: Post) -> dict:
    """Created the update endpoint

    Args:
        _id (int): The id of the post
        _new_post (Post): The data to update the post

    Raises:
        HTTPException: A not found exception is raised when the post is not found

    Returns:
        dict: A message is shown when the logic is successfully run
    """
    cursor.execute(
        """UPDATE posts SET title= %s, content = %s, published=%s WHERE id = %s""", (
            _new_post.title, _new_post.content, _new_post.published, _id)
    )

    _updated_post = cursor.fetchone()

    conn.commit()

    return {"post": _updated_post}
