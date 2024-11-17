import os
import logging
from datetime import datetime
from aiogram import Router, F, html, Bot
from aiogram.utils import markdown
from aiogram.utils.markdown import bold, italic, text, code, pre
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto, LinkPreviewOptions
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from community_telegram_bot.database.models import friendships_models as mds 
from community_telegram_bot.database.requests import friendships_requests as rq
from community_telegram_bot.database.requests import user_requests as urq
from community_telegram_bot.database.database import AsyncSessionLocal
from community_telegram_bot.markups import friendships_markup as nav 
from community_telegram_bot.utilities import geolocation
from dotenv import load_dotenv



# friendships_router = Router(name=__name__)


class Friends(StatesGroup):
    choice = State()
    searching = State()
    bio_overview = State()

class Bio(StatesGroup):
    name = State()
    age = State()
    gender = State()
    bio = State()
    photo1 = State()
    photo2 = State()
    photo3 = State()
    location = State()

class NewBio():
    def __init__(self, user_id, name, age,  gender, bio, city, region = None, country = None, latitude = None, longitude = None) -> None:        
        self.user_id = user_id
        self.name = name
        self.age = age
        self.gender = mds.GenderEnum.MAN if gender == "man" else mds.GenderEnum.WOMAN
        self.bio = bio
        self.city = city
        self.region = region
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

search_funcitons_map = { # execute appropriate function depending on the city_search value in search filter
    True: rq.get_next_bio_by_id_with_city,
    False: rq.get_next_bio_by_id_without_city
}

# --- HELPER FUNCTIONS ---
async def profile_summary(bio, photos):
    summary = markdown.text( #👩🏽👨🏽
            markdown.text(f'{define_gender(bio.gender)}'),
            markdown.hbold(f'{bio.profile_name}'),
            markdown.hunderline(f'{bio.profile_age}'),
            markdown.hitalic(f'- {bio.profile_bio}'),
            markdown.hblockquote(f'{bio.profile_city}')
            )
    media = []
    # media = [InputMediaPhoto(media=photos[0].photo_id)]
    for photo in photos:
        media.append(InputMediaPhoto(media=photo.photo_id))
    media[-1].caption = summary
    return media

# @friendships_router.message()
# async def empty_input(message: Message):
#     await message.answer("I don't understand you")

def define_gender(gender_enum: mds.GenderEnum):
    if gender_enum.MAN:
        return '👨🏼'
    elif gender_enum.WOMAN:
        return '👩🏼'
    else:
        return ''