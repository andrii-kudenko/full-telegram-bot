from . import *
from .friendships_bio_handler import new_bio_by_query

friendships_search_router = Router(name=__name__)

#* --- SEARCH ---
@friendships_search_router.callback_query(nav.FriendsCallback.filter(F.action == "search"))
async def search_by_query(query: CallbackQuery, state: FSMContext, bot:Bot):
    await bot.send_message(query.message.chat.id, "Test Hello")
    user_id = query.from_user.id
    await query.answer("Searching")
    updated_keyboard = await nav.create_blank_keyboard("Search 🔎")
    await query.message.edit_reply_markup(reply_markup=updated_keyboard)
    async with AsyncSessionLocal() as session: # Check if my bio exists
        print(query.message.from_user.id)
        my_bio = await rq.get_my_bio_by_user_id_without_photos(session, user_id)
        print('My bio id:', my_bio.id)
        if my_bio:
            print("IN BIO")
            await rq.update_my_city_search(session, my_bio.id, True) #TODO implement the function
        else:
            print("NOT BIO")
            await query.answer("No Bio")
            await query.message.answer("You do not have a profile for this app. Let's create one")
            await new_bio_by_query(query, state) # TODO deal with new bio
            
    await query.message.answer("Searching...", reply_markup=nav.likeMenu)
    await state.set_state(Friends.searching)
    async with AsyncSessionLocal() as session: # Get next bio
        my_bio_search_filter = await rq.get_my_search_filter(session, user_id) #TODO add this function
        bio, photos = await rq.get_next_bio_by_id_with_city(session, my_bio_search_filter.search_id_list, my_bio_search_filter.city) #TODO change the parameters
        if bio:
            await query.message.answer("Searching...", reply_markup=nav.likeMenu)
            print(bio.id, bio.profile_name)
            summary = markdown.text(
            markdown.hbold(f'{bio.profile_name}'),
            markdown.hunderline(f'{bio.profile_age} - '),
            markdown.hitalic(f'{bio.profile_bio}'),
            markdown.hblockquote(f'{bio.profile_city}')
            )
            media = []
            for photo in photos:
                media.append(InputMediaPhoto(media=photo.photo_id))
            media[-1].caption = summary
            await query.message.answer_media_group(media=media)
            # Update my search id
            updated = await rq.update_my_search_id(session, my_bio_search_filter.id, bio.id) #TODO implement the function
            print('UPDATED', updated)
        elif bio is None:
            await query.message.answer("Searching...")
            await query.message.answer("No more profiles", reply_markup=ReplyKeyboardRemove())
            await query.message.answer("Would you like to search beyond your city?", reply_markup=nav.askToSearchBeyondMenu.as_markup())
            return
        else:
            await query.message.answer("Searching...")
            await query.message.answer("No more profiles", reply_markup=ReplyKeyboardRemove())
            await query.message.answer("You can come later to see new users' profiles", reply_markup=nav.homeChoiceMenu.as_markup())

@friendships_search_router.callback_query(nav.FriendsCallback.filter(F.action == "search_beyond"))
async def search_beyond_by_query(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    await query.answer("Searching beyond")
    updated_keyboard = await nav.create_blank_keyboard("Search beyond city 🔎")
    await query.message.edit_reply_markup(reply_markup=updated_keyboard)
    async with AsyncSessionLocal() as session: # Check if my bio exists
        print(query.message.from_user.id)
        my_bio = await rq.get_my_bio_by_user_id_without_photos(session, user_id)
        print('My bio id:', my_bio.id, 'Search id:', my_bio.search_id)
        if my_bio:
            print("IN BIO")
            await rq.update_my_city_search(session, my_bio.id, False)
        else:
            print("NOT BIO")
            await query.answer("No Bio")
            await query.message.answer("You do not have a profile for this app. Let's create one")
            await new_bio_by_query(query, state) # TODO deal with new bio
            
    await query.message.answer("Searching...", reply_markup=nav.likeMenu)
    await state.set_state(Friends.searching)
    async with AsyncSessionLocal() as session: # Get next bio
        my_bio_search_filter = await rq.get_my_search_filter(session, user_id) #TODO add this function
        bio, photos = await rq.get_next_bio_by_id_with_city(session, my_bio_search_filter.search_id_list, my_bio_search_filter.city) #TODO change the parameters
        # my_bio = await rq.get_my_bio_by_user_id_without_photos(session, user_id)
        # bio, photos = await rq.get_next_bio_by_id_without_city(session, my_bio.beyond_city_search_id, my_bio.id, my_bio.profile_city)
        if bio:
            await query.message.answer("Searching...", reply_markup=nav.likeMenu)
            print(bio.id, bio.profile_name)
            summary = markdown.text(
            markdown.hbold(f'{bio.profile_name}'),
            markdown.hunderline(f'{bio.profile_age} - '),
            markdown.hitalic(f'{bio.profile_bio}'),
            markdown.hblockquote(f'{bio.profile_city}')
            )
            media = []
            for photo in photos:
                media.append(InputMediaPhoto(media=photo.photo_id))
            media[-1].caption = summary
            await query.message.answer_media_group(media=media)
            # Update my search id
            updated = await rq.update_my_search_id(session, my_bio_search_filter.id, bio.id)
            print('UPDATED', updated)
        elif bio is None:
            await query.message.answer("Searching...")
            await query.message.answer("No more profiles", reply_markup=ReplyKeyboardRemove())
            await query.message.answer("You can come later to see new users' profiles", reply_markup=nav.homeChoiceMenu.as_markup())
        else:
            await query.message.answer("Searching...")
            await query.message.answer("No more profiles", reply_markup=ReplyKeyboardRemove())
            await query.message.answer("You can come later to see new users' profiles", reply_markup=nav.homeChoiceMenu.as_markup())

# --- LIKE/DISLIKE ---
@friendships_search_router.message(Friends.searching, F.text == "👍")
async def searching_like(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as session: # Get my bio_id and my search_id
        # my_bio = await rq.get_my_bio_by_user_id_without_photos(session, user_id)
        my_bio_search_filter = await rq.get_my_search_filter(session, user_id) #TODO add this function
        # await message.answer(f'Bio: {my_bio.id} Search: {my_bio.search_id}')
        # print('My bio id:', my_bio.id, 'Search id:', my_bio.search_id)
    # async with AsyncSessionLocal() as session: # Check for a match, with further functionalities
        # print('IN MATCH My bio id:', my_bio.id, 'Search id:', my_bio.search_id)
        # match = await rq.like_user(session, my_bio.id, my_bio.search_id)
        # if match: # Send a message to the user that liked profile, and send a message to a user who was liked and matched
        #     await message.answer("It's a match!")
        #     matched_profile, matched_photos = await rq.get_bio_by_id(session, my_bio.search_id)
        #     matched_profile_info = await bot.get_chat(matched_profile.user_id)
        #     matched_profile_username = matched_profile_info.username
        #     my_profile, my_photos = await rq.get_bio_by_id(session, my_bio.id)
        #     my_profile_info = await bot.get_chat(my_profile.user_id)
        #     my_profile_username = my_profile_info.username
        #     profile = await profile_summary(matched_profile, matched_photos)
        #     await message.answer_media_group(media=profile)
        #     await message.answer(markdown.text(
        #         markdown.text('Go start conversation with 👉🏼'),
        #         markdown.hlink(f'{matched_profile.profile_name} 💬', f'https://t.me/{matched_profile_username}')
        #     ), link_preview_options=LinkPreviewOptions(is_disabled=True))
        #     await bot.send_message(matched_profile.user_id, markdown.text(
        #         markdown.text("You've got a match ❤️‍🔥\n"),
        #         markdown.text("\bGo start conversation with 👉🏼"),
        #         markdown.hlink(f'{my_profile.profile_name} 💬', f'https://t.me/{my_profile_username}')
        #     ), link_preview_options=LinkPreviewOptions(is_disabled=True))
    async with AsyncSessionLocal() as session: # Update search_id, continue with next bio
        # print('IN SEARCH My bio id:', my_bio.id, 'Search id:', my_bio.search_id)
        bio, photos = await search_funcitons_map[my_bio_search_filter.city_search](session, my_bio_search_filter.search_id_list, my_bio_search_filter.city) #TODO change the parameters
        # bio, photos = await search_funcitons_map[my_bio.city_search](session, my_bio.search_id, my_bio.id, my_bio.profile_city)
        # print('IN SEARCH My bio id:', my_bio.id, 'Search id:', my_bio.search_id)
        if bio: # make inputs for photos
            print(bio.id, bio.profile_name)
            summary = markdown.text(
            markdown.hbold(f'{bio.profile_name}'),
            markdown.hunderline(f'{bio.profile_age} - '),
            markdown.hitalic(f'{bio.profile_bio}'),
            markdown.hblockquote(f'{bio.profile_city}')
            )
            media = []
            for photo in photos:
                media.append(InputMediaPhoto(media=photo.photo_id))
            media[-1].caption = summary
            await message.answer_media_group(media=media)
            # updated = await update_funcitons_map[my_bio.city_search](session, my_bio.id, bio.id)
            updated = await rq.update_my_search_id(session, my_bio_search_filter.id, bio.id)
            print('UPDATED', updated)
        elif bio is None:
            if my_bio_search_filter.city_search:
                await message.answer("No more profiles", reply_markup=ReplyKeyboardRemove())
                await message.answer("Would you like to search beyond your city?", reply_markup=nav.askToSearchBeyondMenu.as_markup())
            else:
                await message.answer("Cool, that's it. You've viewed all available profiles 👏", reply_markup=ReplyKeyboardRemove())
                await message.answer("Now you can chill and wait until someone finds your profile interesting", reply_markup=nav.homeChoiceMenu.as_markup())
        else:
             await message.answer("Cool, that's it. You've viewed all available profiles 👏", reply_markup=ReplyKeyboardRemove())
             await message.answer("Now you can chill and wait until someone finds your profile interesting", reply_markup=nav.homeChoiceMenu.as_markup())

@friendships_search_router.message(Friends.searching, F.text == "👎")
async def searching_dislike(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as session: # Get my bio_id and my search_id
        my_bio_search_filter = await rq.get_my_search_filter(session, user_id) #TODO add this function
        # my_bio = await rq.get_my_bio_by_user_id_without_photos(session, user_id)
        # print('My bio id:', my_bio.id, 'Search id:', my_bio.search_id)
    async with AsyncSessionLocal() as session: # Update search_id, continue with next bio
        # bio, photos = await search_funcitons_map[my_bio.city_search](session, my_bio.search_id, my_bio.id, my_bio.profile_city)
        bio, photos = await search_funcitons_map[my_bio_search_filter.city_search](session, my_bio_search_filter.search_id_list, my_bio_search_filter.city) #TODO change the parameters
        if bio:
            print(bio.id, bio.profile_name)
            summary = markdown.text(
            markdown.hbold(f'{bio.profile_name}'),
            markdown.hunderline(f'{bio.profile_age} - '),
            markdown.hitalic(f'{bio.profile_bio}'),
            markdown.hblockquote(f'{bio.profile_city}')
            )
            media = []
            for photo in photos:
                media.append(InputMediaPhoto(media=photo.photo_id))
            media[-1].caption = summary
            await message.answer_media_group(media=media)
            # updated = await update_funcitons_map[my_bio.city_search](session, my_bio.id, bio.id)
            # updated = await rq.update_my_search_id(session, my_bio.id, bio.id)
            updated = await rq.update_my_search_id(session, my_bio_search_filter.id, bio.id)

            print('UPDATED', updated)
        elif bio is None:
            if my_bio_search_filter.city_search:
                await message.answer("No more profiles", reply_markup=ReplyKeyboardRemove())
                await message.answer("Would you like to search beyond your city?", reply_markup=nav.askToSearchBeyondMenu.as_markup())
            else:
                await message.answer("Cool, that's it. You've viewed all available profiles 👏", reply_markup=ReplyKeyboardRemove())
                await message.answer("Now you can chill and wait until someone finds your profile interesting", reply_markup=nav.homeChoiceMenu.as_markup())
        else:
             await message.answer("Cool, that's it. You've viewed all available profiles 👏", reply_markup=ReplyKeyboardRemove())
             await message.answer("Now you can chill and wait until someone finds your profile interesting", reply_markup=nav.homeChoiceMenu.as_markup())

