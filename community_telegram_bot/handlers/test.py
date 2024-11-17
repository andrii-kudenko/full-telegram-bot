# from .friendships import gmaps
import requests
from requests.structures import CaseInsensitiveDict

def get_location_by_lat_long(latitude, longitude)->dict: # Access the attributes like location['city], location['state] 
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&limit=3&format=json&apiKey=...."
    # Headers
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    result = resp.json() # returns 3 addresses
    print(result)
    address1 = result['results'][0] # access the first address
    return address1


if __name__ == "__main__":
    # Uncomment this to run the function when this script is executed directly
    pass
    # reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    # print(reverse_geocode_result)