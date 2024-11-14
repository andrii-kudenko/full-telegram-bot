import os
import googlemaps
from datetime import datetime
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
import googlemaps.geocoding
from community_telegram_bot.database.models import friendships_models as mds 
from community_telegram_bot.database.requests import friendships_requests as rq
from community_telegram_bot.database.database import AsyncSessionLocal
from community_telegram_bot.markups import friendships_markup as nav 
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)



friendships_router = Router(name=__name__)

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
    def __init__(self, user_id, name, age, bio, gender, city, region = None, country = None, latitude = None, longtitude = None) -> None:        
        self.user_id = user_id
        self.name = name
        self.age = age
        self.bio = bio
        self.gender = gender
        self.city = city
        self.region = region
        self.country = country
        self.latitude = latitude
        self.longtitude = longtitude

search_funcitons_map = { # execute appropriate function depending on the city_search value in search filter
    True: rq.get_next_bio_by_id_with_city,
    False: rq.get_next_bio_by_id_without_city
}