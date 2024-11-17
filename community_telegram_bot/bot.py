import logging 
import asyncio
import sys

from aiogram import Bot, Dispatcher, html, types, Router, F
from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, MessageEntityType
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardRemove,
                           UserProfilePhotos, BotDescription, Chat, FSInputFile, MessageEntity, CallbackQuery)
from aiogram.methods import SendMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.methods.send_media_group import SendMediaGroup
from aiogram.fsm.context import FSMContext

from community_telegram_bot.database.database import AsyncSessionLocal
from community_telegram_bot.handlers.friendships.friendships_routers import friendships_router

from community_telegram_bot.database.requests import user_requests as urq

from dotenv import load_dotenv
import os

# *Load Bot Info
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# *Create dispathcer
dp = Dispatcher()
# *Create main router
main_router = Router(name=__name__)
dp.include_routers(main_router, friendships_router)

# *Main router handler
@main_router.message(CommandStart())
async def command_start_handler(message: Message):
    async with AsyncSessionLocal() as session:
        user = await urq.get_user_by_user_id(session, message.from_user.id)
        if user is None:
            user = await urq.create_user(session, message.from_user.id, message.from_user.full_name)
            await message.reply(f"Welcome, {message.from_user.full_name}")
        else:
            await message.reply(f"Welcome back, {message.from_user.full_name}")
    # async with AsyncSessionLocal() as session:


async def main() -> None:    
    try:
        await bot.set_my_commands(commands=[BotCommand(command="/start", description="Start bot"),
                              BotCommand(command="/home", description="Go home"),
                              BotCommand(command="/jobs", description="Look for job"),
                              BotCommand(command="/friends", description="Look for friends"),
                              BotCommand(command="/help", description="Get help")
                              ])
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")