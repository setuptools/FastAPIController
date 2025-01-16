import fastapi

from fastapi import Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
import json

from redis.asyncio import Redis

import asyncio

from colorama import init
from typing import List , Optional

init()

with open("config.json","r+") as cfg_file:
    config = json.load(cfg_file)
cfg_file.close()

app = fastapi.FastAPI()

templates = Jinja2Templates(directory= "templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class MessageData(BaseModel):
    message: str
    user_ids: str
    urls: Optional[list] = None

async def get_from_bot_user_ids():
    redis = Redis.from_url("redis://localhost:6379", decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe("user_ids")

    async for message in pubsub.listen():
        if message["type"] == "message":
            app.state.user_ids = message["data"]

@app.on_event("startup")
async def startup():
    app.state.redis = await Redis(host = config['redis']['host'] , port = config['redis']['port'], decode_responses= True)
    app.state.user_ids = ""

    asyncio.create_task(get_from_bot_user_ids())



@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()

@app.get("/users_ids")
async def get_users_ids():
    return app.state.user_ids

@app.get("/")
async def start():
    return {"connection":True}

@app.post("/send_messages")
async def send_mesasges(data: MessageData):
    await app.state.redis.flushall()

    await app.state.redis.publish("bot_messaging", data.message)
    await app.state.redis.publish("bot_user_ids", data.user_ids)
    await app.state.redis.publish("bot_urls", ",".join(data.urls))

    return {"message":data.message , "users":data.user_ids}

@app.get("/menu", response_class= HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse("site.html", {"request": request})
    

