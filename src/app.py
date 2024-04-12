from http import HTTPStatus
from fastapi import FastAPI, Request, Response
from telegram import Update

from bot.bot import bot


app = FastAPI()


@app.post('/')
async def bot_webhook(request: Request):
    req = await request.json()
    update = Update.de_json(req, bot.bot)
    await bot.process_update(update)
    return Response(status_code=HTTPStatus.OK)
