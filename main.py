"""The entrypoint for the backend"""

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    """Created the Post class

    Args:
        BaseModel (Class): The parant class of Post
    """
    title: str
    content: str


@app.get("/")
async def root() -> dict:
    """The root api endpoint

    Returns:
        dict: A message to show successful execution
    """
    return {"Message": "Hello World"}


@app.post("/createpost")
async def create_post(payload: Post) -> dict:
    """A dummy endpoint to create a post

    Returns:
        dict: The message to show successful logic execution
    """
    print(payload)
    return {"new_post": f"title {payload['I came']}:content {payload['I praised the lord']}"}
