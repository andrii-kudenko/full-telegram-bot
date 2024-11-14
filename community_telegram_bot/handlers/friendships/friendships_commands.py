import logging
from aiogram import Router, F, html
from aiogram.types import Command, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from . import nav, Bio


from . import friendships_router

@friendships_router.message(Command("friends", prefix=("!/")))
async def start_friends(message: Message, state: FSMContext):    
    text = " " * 25 + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    await message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())
@friendships_router.callback_query(nav.MenuCallback.filter(F.menu == "start_friends"))
async def start_friends_by_query(query: CallbackQuery, callback_data: nav.MenuCallback, state: FSMContext):
    await query.answer("Friends")
    updated_keyboard = await nav.create_blank_keyboard("Friends 🤼")
    await query.message.edit_reply_markup(reply_markup=updated_keyboard)
    text = " " * 25 + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    await query.message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())

@friendships_router.message(Bio.name, Command("cancel", prefix=("!/")))
@friendships_router.message(Bio.age, Command("cancel", prefix=("!/")))
@friendships_router.message(Bio.bio, Command("cancel", prefix=("!/")))
@friendships_router.message(Bio.photo1, Command("cancel", prefix=("!/")))
@friendships_router.message(Bio.photo2, Command("cancel", prefix=("!/")))
@friendships_router.message(Bio.photo3, Command("cancel", prefix=("!/")))
@friendships_router.message(Bio.location, Command("cancel", prefix=("!/")))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    
    await message.answer(
        "Cancelled. Choose the action:",
        reply_markup=nav.friendsChoiceMenu.as_markup(),
    )
    # await set_default_commands(id=message.from_user.id)
@friendships_router.message(Bio.name, Command("back", prefix=("!/")))
@friendships_router.message(Bio.age, Command("back", prefix=("!/")))
@friendships_router.message(Bio.bio, Command("back", prefix=("!/")))
@friendships_router.message(Bio.photo1, Command("back", prefix=("!/")))
@friendships_router.message(Bio.photo2, Command("back", prefix=("!/")))
@friendships_router.message(Bio.photo3, Command("back", prefix=("!/")))
@friendships_router.message(Bio.location, Command("back", prefix=("!/")))
async def back_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Bio.name:
            await state.clear()
            text = " " * 25 + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
            await message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())
    elif current_state == Bio.age:
            await state.set_state(Bio.name)
            await message.answer("Send me your name")
    elif current_state == Bio.bio:
            await state.set_state(Bio.age)
            await message.answer("Send me your age")
    elif current_state == Bio.photo1:
            await state.set_state(Bio.bio)
            await message.answer("Send me your bio")
    elif current_state == Bio.photo2:
            await state.set_state(Bio.photo1)
            await message.answer("Send me your photo")
    elif current_state == Bio.photo3:
            await state.set_state(Bio.photo2)
            await message.answer("Send me another photo")
    elif current_state == Bio.location:
            await state.set_state(Bio.photo3)
            await message.answer("Send me another photo")