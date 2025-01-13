from fastapi import FastAPI

from rjapi.models.post import UserPost, UserPostIn

app = FastAPI()


post_table = {}


@app.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()

    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}

    post_table[last_record_id] = new_post

    return new_post


@app.get("/post", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())
