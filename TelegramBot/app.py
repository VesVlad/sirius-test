import os
import urllib
import random
import requests
from model import model_whisper
from telegram import Update
from config import TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from db_functions import *
from sqlalchemy import create_engine, inspect
from schema import Base
import re

engine = create_engine("postgresql+psycopg2://bot_user:trybetter@postgres:5432/tinkoff_bot_db")
if inspect(engine).has_table("users", schema="public") is False:
    Base.metadata.create_all(engine)

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="""✨✨✨ПрИвЕт-ы!✨✨✨\nМеня зовут молЧАТ, я создан для того, чтобы ты мог скоротать время, общаясь со мной, пока ты летишь в Сочи!
                                           \nЧтобы начать диалог со мной, просто напиши что-нибудь!😎 \n Чтобы посмотреть, что я умею, напиши /help""")

async def help(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="""Что умеет бот?👾\n Отвечать на текстовые и аудиосообщения 💬 
                                   \n Использует для лучшего общения контекст и чистит его с помощью команды /clean 🧹""")

async def answer(update: Update, context: CallbackContext):
    user_id = update.message.from_user['username']
    add_user(user_id)
    if len(update.message.text) != 0:
        msg = update.message.text
        msg = urllib.parse.unquote(msg)
        curr_context = get_context(user_id)
        curr_context = curr_context if curr_context.endswith("@@ПЕРВЫЙ@@") else curr_context + "@@ПЕРВЫЙ@@"
        curr_context = curr_context.lstrip() + f" {msg}" + "@@ВТОРОЙ@@"
        answer = requests.get(f"http://server:4321/api/{curr_context}")
        answer.encoding = "utf-8"
        remove_context(user_id)
        add_context(user_id, answer.text)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=answer.text.split("@@ВТОРОЙ@@")[-1].split("@@ПЕРВЫЙ@@")[0])

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="пустое сообщение!")

async def answer_audio(update: Update, context: CallbackContext):
    user_id = update.message.from_user['username']
    add_user(user_id)
    audiofile = await context.bot.get_file(update.message.voice.file_id)
    output = random.randint(1, 1000)
    await audiofile.download_to_drive(f"{output}.wav")
    try:
        msg = model_whisper.transcribe(f"{output}.wav")['text']
        curr_context = get_context(user_id)
        curr_context = curr_context if curr_context.endswith("@@ПЕРВЫЙ@@") else curr_context + "@@ПЕРВЫЙ@@"
        curr_context = curr_context + f" {msg}" + " @@ВТОРОЙ@@"
        answer = requests.get(f"http://server:4321/api/{curr_context}")
        answer.encoding = "utf-8"
        remove_context(user_id)
        add_context(user_id, answer.text)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=answer.text.split("@@ВТОРОЙ@@")[-1].split("@@ПЕРВЫЙ@@")[0])
        os.remove(f"{output}.wav")
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось обработать твое голосовое сообщение, попробуй еще раз!🥹")
        os.remove(f"{output}.wav")

async def clean(update: Update, context: CallbackContext):
    user_id = update.message.from_user['username']
    remove_context(user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="контекст обновлен!🧹")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    dialog_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), answer)
    audio_handler = MessageHandler(filters.VOICE, answer_audio)
    clean_handler = CommandHandler('clean', clean)

    app.add_handler(start_handler)

    app.add_handler(help_handler)

    app.add_handler(dialog_handler)

    app.add_handler(audio_handler)

    app.run_polling()