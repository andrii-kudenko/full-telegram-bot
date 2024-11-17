from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import BigInteger, update
from ..models import Bio, BioPhoto, Like, GenderEnum, FriendshipSearchFilter


#* --- CREATE BIO ---
async def add_bio_to_user_by_user_id(db: AsyncSession, bio, photos):
    # Fetch existing bio with associated photos, if any
    result = await db.execute(select(Bio).options(joinedload(Bio.photos)).filter(Bio.user_id == bio.user_id))
    existing_bio = result.scalars().first()

    # Remove existing bio and associated photos, if found
    if existing_bio:
        await remove_existing_photos(db, existing_bio)
        await db.delete(existing_bio)
        await db.commit()

    # Create a new Bio object
    new_bio = Bio(
        user_id=bio.user_id,
        profile_name=bio.name,
        profile_age=int(bio.age),
        gender = bio.gender,
        profile_bio=bio.bio,
        profile_city=bio.city,
        profile_region = bio.region,
        profile_country = bio.country,
        latitude=str(bio.latitude) if bio.latitude else None,
        longitude=str(bio.longitude) if bio.longitude else None,
    )

    # Add the new bio to the database
    db.add(new_bio)
    await db.commit()
    await db.refresh(new_bio)

    # Add photos to the newly created bio
    await add_photos_to_bio(db, new_bio.id, photos)
    # Create search filter for the new bio
    await create_search_filter(db, new_bio.user_id, new_bio.id)
    return new_bio

#* --- GET BIO ---
async def get_my_bio_by_user_id_with_photos(db: AsyncSession, user_id: BigInteger):
    result = await db.execute(select(Bio).options(joinedload(Bio.photos)).filter(Bio.user_id == user_id))
    my_bio = result.scalars().first()
    photos = []
    if my_bio:
        photos = my_bio.photos
    return my_bio, photos
async def get_my_bio_by_user_id_without_photos(db: AsyncSession, user_id: BigInteger):
    result = await db.execute(select(Bio).filter(Bio.user_id == user_id))
    my_bio = result.scalars().first()
    return my_bio

#* --- HANDLE PHOTOS ---
async def add_photos_to_bio(db: AsyncSession, bio_id: int, photos: list):
    print("IM IN ADDING PHOTOS")
    for photo in photos:
        new_photo = BioPhoto(bio_id=bio_id, photo_id=photo)
        db.add(new_photo)
    await db.commit()
async def remove_existing_photos(db: AsyncSession, existing_bio: Bio):
    print("IM IN REMOVING PHOTOS")
    await db.refresh(existing_bio)
    for photo in existing_bio.photos:
        await db.delete(photo)
    await db.commit()

#* --- HANDLE SEARCH ---
async def get_next_bio_by_id_with_city(db: AsyncSession, bio_id: int, exclude_bio_id: int, city: str): # Add a calculator to calculate distances
    cities = [city.strip().lower()]
    stmt = select(Bio).options(joinedload(Bio.photos)).filter(Bio.id > bio_id).filter(Bio.id != exclude_bio_id).filter(Bio.profile_city.in_(cities)).order_by(Bio.id).limit(1)
    result = await db.execute(stmt)
    bio = result.scalars().first()
    photos = []
    if bio:
        photos = bio.photos
    return bio, photos
async def get_next_bio_by_id_without_city(db: AsyncSession, bio_id: int, exclude_bio_id: int, city: str): # Add a calculator to calculate distances
    cities = [city.strip().lower()]
    stmt = select(Bio).options(joinedload(Bio.photos)).filter(Bio.id > bio_id).filter(Bio.id != exclude_bio_id).filter(Bio.profile_city.in_(cities)).order_by(Bio.id).limit(1)
    result = await db.execute(stmt)
    bio = result.scalars().first()
    photos = []
    if bio:
        photos = bio.photos
    return bio, photos

#* --- HANDLE SEARCH FILTER ---
async def create_search_filter(db: AsyncSession, user_id, bio_id):
    # Create a new Bio object
    new_search_filter = FriendshipSearchFilter(
        user_id=user_id,
        bio_id=bio_id
    )
    # Add the new filter to the database
    db.add(new_search_filter)
    await db.commit()
    await db.refresh(new_search_filter)

#* --- HANDLE UPDATES ---
async def update_my_search_id(db: AsyncSession, bio_id, search_id):
    pass
async def update_my_city_search(db: AsyncSession, my_bio_id, new_city_search: bool):
    pass

#TODO add a develpment function to add dummy data to the database