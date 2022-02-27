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
    places = gmaps.find_place(input=name+" "+address, input_type="textquery")
    # assume we take the first result
    place = places[0]
    print()
    print(place)
    return 0,{}