import os
from dotenv import load_dotenv
import googlemaps
import requests
import json
import urllib
from fuzzywuzzy import fuzz
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

def gmapsplaceid_(business):
    name = business["name"]
    address = business["address"]
    places = gmaps.find_place(input=name+" "+address, input_type="textquery")["candidates"]
    # assume we take the first result
    if len(places) > 1: print("[WARN] More than one result for google listings, assuming first")
    return places[0]["place_id"]

def gmapspresence(business):
    place = gmapsplaceid_(business)
    print()
    details = gmaps.place(place)["result"]
    # from these details we can get
    googlerating = details["rating"]
    website = details["website"]
    phonenumber = details["formatted_phone_number"]
    numofratings = details["user_ratings_total"]
    return 0,{}

def googleknowledgebase(business):
    endpoint = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        "key": API_KEY,
        "query": business["name"],
        "limit": 1,
        "indent": True
    }
    req_url = endpoint + "?" + urllib.parse.urlencode(params)
    
    res = json.loads(urllib.request.urlopen(req_url).read())
    result = res["itemListElement"][0] if res["itemListElement"] else {}
    if not result: return 0
    
    similarity = fuzz.ratio(business["name"], result["result"]["name"])
    return similarity if similarity > 90 else 0