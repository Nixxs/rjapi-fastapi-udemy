from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int
    ConfigDict(from_attributes=True)


# what the user provides in the payload
class CommentIn(BaseModel):
    body: str
    post_id: int


# what the response is back to the user
class Comment(CommentIn):
    id: int
    ConfigDict(from_attributes=True)


class UserPostWithcomments(BaseModel):
    post: UserPost
    comments: list[Comment]
