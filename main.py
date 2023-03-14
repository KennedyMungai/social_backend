"""The entrypoint for the backend"""

from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from random import randrange

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


def find_post(_id: int):
    """A function to find a post inside the my_posts array

    Args:
        _id (int): The id of the post

    Returns:
        Post: The found post
    """
    for post in my_posts:
        if post["id"] == _id:
            return post


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


@app.get("/posts/{_id}")
async def retrieve_one_post(_id: int) -> dict:
    """An endpoint to retrieve a specified post

    Args:
        _id (int): The id of the post

    Returns:
        dict: Outputs the post data
    """
    _post = find_post(_id)

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {_id} was not found")
    else:
        return _post


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_post(_post: Post) -> dict:
    """The create post endpoint

    Args:
        _post (Post): The post

    Returns:
        dict: A returned dictionary to show successful execution of the logic
    """
    _post_dict = _post.dict()
    _post_dict["id"] = randrange(0, 1000000)
    my_posts.append(_post_dict)

    return {"data": _post_dict}


@app.delete("/posts/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_post(_id: int) -> dict:
    """An endpoint for deleting posts

    Args:
        _id (int): The id of the post

    Raises:
        HTTPException: A not found exception is raised if the post is not found in my_posts

    Returns:
        dict: A message to show the successful execution of the code
    """
    _post = find_post(_id)

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post of id: {_id} does not exist")

    _post_index = my_posts.index(_post)
    my_posts.pop(_post_index)

    return {"message": "The post has been successfully deleted"}
