"""The entrypoint for the backend"""

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    """Created the Post class

    Args:
        BaseModel (Class): The parent class of Post
    """
    title: str
    content: str
    published: Optional[bool] = True


@app.get("/")
async def root() -> dict:
    """The root api endpoint

    Returns:
        dict: A message to show successful execution
    """
    return {"Message": "Hello World"}


@app.post("/createpost")
async def create_post(_new_post: Post) -> dict:
    """A dummy endpoint to create a post

    Returns:
        dict: The message to show successful logic execution
    """
    print(_new_post.published)
    return {"data": "new post"}
