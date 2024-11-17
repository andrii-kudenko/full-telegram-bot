from . import *

friendships_empty_router = Router(name=__name__)

@friendships_empty_router.message()
async def empty_input(message: Message):
    await message.answer("I don't understand you")

@friendships_empty_router.callback_query(nav.BlankCallback.filter())
async def handle_blank(query: CallbackQuery, callback_data: nav.BlankCallback):
    text = callback_data.text
    await query.answer(f"{text}")