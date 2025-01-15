from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


# what the user provides in the payload
class CommentIn(BaseModel):
    body: str
    post_id: int


# what the response is back to the user
class Comment(CommentIn):
    id: int
