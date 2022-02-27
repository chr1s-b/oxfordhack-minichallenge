import os
from dotenv import load_dotenv
import googlemaps
import requests
import json
import urllib
from fuzzywuzzy import fuzz
import re
from datetime import datetime

# load in api key for Google Places API



load_dotenv()
API_KEY = os.environ.get("API_KEY")




print(f"Loaded Google Places API key {API_KEY}")

gmaps = googlemaps.Client(key=API_KEY)

def mobilecompatibility(url):
    global API_KEY;
    """uses google mobile support checker webpage to see if the webpage has mobile support """
    apiUrl = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
    params = {
            'url': url,
            'requestScreenshot': 'false',
            'key': API_KEY
        }

    x = requests.post(apiUrl, data = params)
    data = json.loads(x.text)
    print(data)
    if(data['testStatus'] == {'status': 'COMPLETE'}):
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

#Social Media Checks

def hasFacebook(url):
    data = requests.get(url)
    return ("facebook" in data.text.lower())

def hasTwitter(url):
    data = requests.get(url)
    return ("twitter" in data.text.lower())

def hasInstagram(url):
    data = requests.get(url)
    return ("isntagram" in data.text.lower())

#Get social media urls
def getFacebook(url):
    #Look for 
    #https://www.facebook.com/ ... "
    data = requests.get(url).text
    urlSize = len('https://facebook.com/')
    index = data.index('https://facebook.com/')
    for i in range(index+urlSize,len(data)):
        if(data[i]=="'" or data[i]=='"'):
            return data[index:i]
        data = requests.get(url).text
    #look again for https://www. 
    urlSize = len('https://www.facebook.com/')
    index = data.index('https://www.facebook.com/')
    for i in range(index+urlSize,len(data)):
        if(data[i]=="'" or data[i]=='"'):
            return data[index:i]

def getTwitter(url):
    #Look for 
    #https://twitter.com/ ... "
    data = requests.get(url).text
    urlSize = len('https://twitter.com/')
    index = data.index('https://twitter.com/')
    for i in range(index+urlSize,len(data)):
        if(data[i]=="'" or data[i]=='"'):
            return data[index:i]

    #look again in case they use https://www.twitter.com
    urlSize = len('https://www.twitter.com/')
    index = data.index('https://www.twitter.com/')
    for i in range(index+urlSize,len(data)):
        if(data[i]=="'" or data[i]=='"'):
            return data[index:i]

def getInstagram(url):
    #Look for 
    #https://instagram.com/ ... "
    data = requests.get(url).text
    urlSize = len('https://instagram.com/')
    index = data.index('https://instagram.com/')
    for i in range(index+urlSize,len(data)):
        if(data[i]=="'" or data[i]=='"'):
            return data[index:i]

    #look again in case they use https://www.instagram.com
    urlSize = len('https://www.instagram.com/')
    index = data.index('https://www.instagram.com/')
    for i in range(index+urlSize,len(data)):
        if(data[i]=="'" or data[i]=='"'):
            return data[index:i]

    #Interacting With Social Media


def getInstagramFollowers(igURL):
    r = requests.get(igURL).text
    followers = re.search('"edge_followed_by":{"count":([0-9]+)}',r).group(1)

    print(followers)
>>>>>>> 62c82b1e1b5fcbfecae3991bc563c5878d39bfb7
