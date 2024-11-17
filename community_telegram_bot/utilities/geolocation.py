import requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
import os

load_dotenv()
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_location_by_lat_long(latitude, longitude)->dict: # Access the attributes like location['city], location['state] 

    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&limit=3&format=json&apiKey={GEOAPIFY_API_KEY}"
    # Headers
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    result = resp.json() # returns 3 addresses
    print(result)
    address1 = result['results'][0] # access the first address
    return address1
    # country = address1['country']
    # region = address1['state']
    # city = address1['city']
    # print(address1)
    # print(country)
    # print(region)
    # print(city)