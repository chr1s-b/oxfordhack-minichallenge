import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime

# load in api key for Google Places API
load_dotenv()
API_KEY = os.environ.get("API_KEY")
print(f"Loaded Google Places API key {API_KEY}")

gmaps = googlemaps.Client(key=API_KEY)

def mobilecompatibility(url):
    return 0,{}


def gmapspresence(business):
    name = business["name"]
    address = business["address"]
    place = gmaps.find_place(input=address, input_type="textquery")
    print(place)
    return 0,{}