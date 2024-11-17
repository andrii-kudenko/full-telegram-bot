from . import *
frienships_commands_router = Router(name=__name__)

@frienships_commands_router.message(Command("friends", prefix=("!/")))
async def start_friends(message: Message, state: FSMContext):    
#     text = "&#x200D;" + " " * 25 + "&#x200D;" + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    text = "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    await message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())
@frienships_commands_router.callback_query(nav.MenuCallback.filter(F.menu == "start_friends"))
async def start_friends_by_query(query: CallbackQuery, callback_data: nav.MenuCallback, state: FSMContext):
    await query.answer("Friends")
    updated_keyboard = await nav.create_blank_keyboard("Friends 🤼")
    await query.message.edit_reply_markup(reply_markup=updated_keyboard)
    text = " " * 25 + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    await query.message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())

@frienships_commands_router.message(Bio.name, Command("cancel", prefix=("!/")))
@frienships_commands_router.message(Bio.age, Command("cancel", prefix=("!/")))
@frienships_commands_router.message(Bio.bio, Command("cancel", prefix=("!/")))
@frienships_commands_router.message(Bio.photo1, Command("cancel", prefix=("!/")))
@frienships_commands_router.message(Bio.photo2, Command("cancel", prefix=("!/")))
@frienships_commands_router.message(Bio.photo3, Command("cancel", prefix=("!/")))
@frienships_commands_router.message(Bio.location, Command("cancel", prefix=("!/")))
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
@frienships_commands_router.message(Bio.name, Command("back", prefix=("!/")))
@frienships_commands_router.message(Bio.age, Command("back", prefix=("!/")))
@frienships_commands_router.message(Bio.bio, Command("back", prefix=("!/")))
@frienships_commands_router.message(Bio.photo1, Command("back", prefix=("!/")))
@frienships_commands_router.message(Bio.photo2, Command("back", prefix=("!/")))
@frienships_commands_router.message(Bio.photo3, Command("back", prefix=("!/")))
@frienships_commands_router.message(Bio.location, Command("back", prefix=("!/")))
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


@frienships_commands_router.message(Command("create_users", prefix=("!/")))
async def create_users(message: Message, state: FSMContext):    
#     text = "&#x200D;" + " " * 25 + "&#x200D;" + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    user1 = (637785719, 'Mark')
    user2 = (1363164049, 'Dima')
    user3 = (5479352762, 'Random')
    user4 = (440410516, 'Elena')
    user5 = (370575770, 'Oleg')
    async with AsyncSessionLocal() as session:  
        new_user1 = await urq.create_user(session, user1[0], user1[1])
        new_user2 = await urq.create_user(session, user2[0], user2[1])
        new_user3 = await urq.create_user(session, user3[0], user3[1])
        new_user4 = await urq.create_user(session, user4[0], user4[1])
        new_user5 = await urq.create_user(session, user5[0], user5[1])
    text = "Users created" + " " * 25 + "&#x200D;" + '\n'
    await message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())
@frienships_commands_router.message(Command("create_bios", prefix=("!/")))
async def create_bios(message: Message, state: FSMContext):    
#     text = "&#x200D;" + " " * 25 + "&#x200D;" + "Friends Finder Menu" + " " * 25 + "&#x200D;" + '\n'
    bio1 = NewBio(637785719, 'Mark', 20, mds.GenderEnum.MAN, "Poker", 'Tilburg')
    bio2 = NewBio(1363164049, 'Dima', 15, mds.GenderEnum.MAN, "Dota 2", 'Oakville')
    bio3 = NewBio(5479352762, 'Random', 21, mds.GenderEnum.MAN, "Im a random person", 'New York')
    bio4 = NewBio(440410516, 'Elena', 20, mds.GenderEnum.WOMAN, "I like Andrew's bot", 'Halifax')
    bio5 = NewBio(370575770, 'Oleg', 20, mds.GenderEnum.MAN, "Roblox", 'Toronto')
    async with AsyncSessionLocal() as session:  
        photos = ['AgACAgIAAxkBAAILtGZzlKza_PqsCQTzPxDMtAwynRYrAAIs2DEbuNigS0YrTGsgmrXgAQADAgADeAADNQQ']
        new_bio1 = await rq.add_bio_to_user_by_user_id(session, bio1, photos)
        new_bio2 = await rq.add_bio_to_user_by_user_id(session, bio2, photos)
        new_bio3 = await rq.add_bio_to_user_by_user_id(session, bio3, photos)
        new_bio4 = await rq.add_bio_to_user_by_user_id(session, bio4, photos)
        new_bio5 = await rq.add_bio_to_user_by_user_id(session, bio5, photos)
    text = "Bios created" + " " * 25 + "&#x200D;" + '\n'
    await message.answer(text, reply_markup=nav.friendsChoiceMenu.as_markup())