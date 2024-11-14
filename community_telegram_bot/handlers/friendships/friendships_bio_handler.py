from typing import Any, Dict
import logging
from sqlalchemy import BigInteger
from collections import defaultdict
import threading

from aiogram import Router, F, html
from aiogram.utils import markdown
from aiogram.utils.markdown import bold, italic, text, code, pre
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand, CallbackQuery, InputMediaPhoto, InputFile, LinkPreviewOptions
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# from . import friendships_router, nav, rq, AsyncSessionLocal, Bio, NewBio
from . import *

#* --- MY BIO ---
@friendships_router.callback_query(nav.MenuCallback.filter(F.menu == "my_bio"))
async def my_bio_by_query(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    await query.answer("My Bio")
    # await state.set_state(Friends.bio_overview)
    updated_keyboard = await nav.create_blank_keyboard("My Bio 👤")
    await query.message.edit_reply_markup(reply_markup=updated_keyboard)
    async with AsyncSessionLocal() as session:
        my_bio, photos = await rq.get_my_bio_by_user_id(session, user_id)
        if my_bio:
            summary = markdown.text(
                markdown.hbold(f'{my_bio.profile_name}'),
                markdown.hunderline(f'{my_bio.profile_age} - '),
                markdown.hitalic(f'{my_bio.profile_bio}'),
                markdown.hblockquote(f'{my_bio.profile_city}')
            )
            media = []
            if photos:
                for photo in photos:
                    media.append(InputMediaPhoto(media=photo.photo_id))
                media[-1].caption = summary
            last_message = await query.message.answer_media_group(media=media)
            # await query.message.a("My bio")
            await last_message[-1].answer(text="Choose action", reply_markup=nav.bioChangeMenu.as_markup())
            # await query.message.edit_text(text=summary, reply_markup=nav.bioChangeMenu.as_markup())
        else:
            await query.answer("No Bio")
            await query.message.edit_text("You do not have a profile for this app. Let's create one")
            await new_bio_by_query(query, state)

#* --- NEW BIO ---
@friendships_router.callback_query(nav.FriendsCallback.filter(F.action == "new_bio"))
async def new_bio_by_query(query: CallbackQuery, state: FSMContext):
    await query.answer("Creating New Bio")
    updated_keyboard = await nav.create_blank_keyboard("New Bio 👤")
    await query.message.edit_reply_markup(reply_markup=updated_keyboard)
    await query.message.answer("Creating your profile...\nMind that you can always \nGo /back or /cancel the process")
    await state.set_state(Bio.name)
    await query.message.answer("Type your name:")
    # await set_back_commands(id=query.from_user.id)

#* --- BIO CREATION ---
@friendships_router.message(Bio.name, F.text)
async def profile_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Bio.age)
    await message.answer(f"Nice, {html.bold(message.text)}!\nNow, type your age:")
@friendships_router.message(Bio.age, F.text)
async def profile_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Bio.bio)
    await message.answer(f"Ok, now provide some information about you and your interests:")
@friendships_router.message(Bio.bio, F.text)
async def profile_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await state.set_state(Bio.photo1)
    await message.answer(f"Cool! now provide a photo for your profile:")
@friendships_router.message(Bio.photo1, F.photo)
async def profile_photo1(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    new_photo = await state.update_data(photo1 = file_id)
    await state.set_state(Bio.photo2)
    await message.answer("Nice, you have uploaded one photo. Send another one or just continue with this one", reply_markup=nav.photosUploadingReplyMenu1)
@friendships_router.message(Bio.photo2, F.photo)
async def profile_photo2(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    new_photo = await state.update_data(photo2 = file_id)
    await state.set_state(Bio.photo3)
    await message.answer("Good, now you have 2 photos. Want to add one more?", reply_markup=nav.photosUploadingReplyMenu2)
@friendships_router.message(Bio.photo3, F.photo)
async def profile_photo3(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    new_photo = await state.update_data(photo3 = file_id)
    await state.set_state(Bio.location)
    await message.answer("Cool, now you have 3 photos for you profile", reply_markup=ReplyKeyboardRemove())
    await confirm_photos(message, state)
@friendships_router.message(Bio.photo2, F.text == "Continue with 1/3 photos")
@friendships_router.message(Bio.photo3, F.text == "Continue with 2/3 photos")
async def confirm_photos(message: Message, state: FSMContext):
    await state.set_state(Bio.location)
    await message.answer(f"Finally, provide your location:", reply_markup=nav.locationMenu)
@friendships_router.message(Bio.location, F.location)
@friendships_router.message(Bio.location, F.text)
async def profile_location(message: Message, state: FSMContext):
    if message.location:
        reverse_geocode_result = gmaps.reverse_geocode((message.location.latitude, message.location.longitude))

        # user_location = location.get_location(message.location.latitude, message.location.longitude)
        print(reverse_geocode_result)
        return #TODO very important to finish this part, also first of all to test the api
        # data = await state.update_data(location=user_location[1])
        # print(data["location"])
        # new_bio = NewBio(True, message.from_user.id, data["name"], data["bio"], data["age"], data["location"], message.location.latitude, message.location.longitude)
    else:
        city = message.text.strip().title()
        data = await state.update_data(location=city)
        new_bio = NewBio(False, message.from_user.id, data["name"], data["bio"], data["age"], message.text)
    await state.clear()
    await show_summary(message=message, data=data)
    async with AsyncSessionLocal() as session:  
        photos = []
        photos.append(data["photo1"])
        photos.append(data.get("photo2")) if data.get("photo2") else None
        photos.append(data.get("photo3")) if data.get("photo3") else None
        my_new_bio = await rq.add_bio_to_user_by_id(session, new_bio, photos)
        print("Bio added successfully")
    await message.answer("Cool, now go search for new connections!", reply_markup=nav.friendsReplyChoiceMenu.as_markup())
    # await set_default_commands(id=message.from_user.id)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True):
    name = data["name"]
    bio = data["bio"]
    age = data["age"]
    location = data["location"]
    photos = []
    photos.append(data["photo1"])
    photos.append(data.get("photo2")) if data.get("photo2") else None
    photos.append(data.get("photo3")) if data.get("photo3") else None
    summary = markdown.text(
                markdown.hbold(f'{name}'),
                markdown.hunderline(f'{age} - '),
                markdown.hitalic(f'{bio}'),
                markdown.hblockquote(f'{location}')
            )
    media = []
    # media = [InputMediaPhoto(media=photos[0].photo_id)]
    for photo in photos:
        media.append(InputMediaPhoto(media=photo))
    media[-1].caption = summary
    await message.answer("Your Bio", reply_markup=ReplyKeyboardRemove())
    await message.answer_media_group(media=media)