from fastapi import FastAPI, Request
from chat import ask

app = FastAPI()

@app.post("/")
async def home(request: Request):
    body = await request.json()
    user = body.get("user")
    reply = ask(user)
    return {
        "user": user,
        "reply" : reply
    }