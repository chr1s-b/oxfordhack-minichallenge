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
            'key': "AIzaSyB4hW39-INaUINhqCeaRXkMx87KJGCAYIY"
        }

    x = requests.post(apiUrl, data = params)
    data = json.loads(x.text)
    print(data['test_status'] == {'status': 'COMPLETE'})
    return data['mobileFriendliness'] == 'MOBILE_FRIENDLY'



def gmapspresence(business):
    name = business["name"]
    address = business["address"]
    place = gmaps.find_place(input=address, input_type="textquery")
    print(place)
    return 0,{}