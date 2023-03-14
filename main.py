"""The entrypoint for the backend"""

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

my_posts = [
    {"title": "Title of the first post",
        "content": "Content of the first post", "id": 1},
    {"title": "Title of the second post",
        "content": "Content of the second post", "id": 2}
]


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
    return {"data": my_posts}


@app.post("/createpost")
async def create_post(_post: Post) -> dict:
    """A dummy endpoint to create a post

    Returns:
        dict: The message to show successful logic execution
    """
    # print(_new_post.rating)
    _post_dict = _post.dict()
    return {"data": _post_dict}
