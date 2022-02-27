import os
from dotenv import load_dotenv
import googlemaps
import requests
import json
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



def gmapspresence(business):
    name = business["name"]
    address = business["address"]
    places = gmaps.find_place(input=name+" "+address, input_type="textquery")
    # assume we take the first result
    place = places[0]
    print()
    print(place)
    return 0,{}


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