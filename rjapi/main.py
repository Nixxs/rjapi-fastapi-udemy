from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "omg its working even in azure now."}
