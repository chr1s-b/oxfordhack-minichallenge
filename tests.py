import os
from dotenv import load_dotenv
import googlemaps
import requests
import json
from datetime import datetime

# load in api key for Google Places API
load_dotenv()
API_KEY = os.environ.get("API_KEY")
print(f"Loaded Google Places API key {API_KEY}")

gmaps = googlemaps.Client(key=API_KEY)

def mobilecompatibility(url):
    """uses google mobile support checker webpage to see if the webpage has mobile support """
    apiUrl = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
    params = {
            'url': url,
            'requestScreenshot': 'false',
            'key': API_KEY
        }

    x = requests.post(apiUrl, data = params)
    data = json.loads(x.text)
    if(data['test_status'] == {'status': 'COMPLETE'}):
        return data['mobileFriendliness'] == 'MOBILE_FRIENDLY'
    return False

print(mobilecompatibility("https://hotmail.co.uk"))
print(mobilecompatibility("ayqwq"))

def gmapspresence(business):
    name = business["name"]
    address = business["address"]
    places = gmaps.find_place(input=name+" "+address, input_type="textquery")
    # assume we take the first result
    place = places[0]
    print()
    print(place)
    return 0,{}