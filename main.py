import json
from tests import *

with open("input-alt.json", 'r') as f:
    contents = f.read()

businesses = json.loads(contents)

# load weights
weights = {}
with open("weights.json", 'r') as f:
    weights = json.loads(f.read())


def rate_business(business):
    '''Given a name and address of a business, returns a rating between 0.0 and 10.0 and the details that compose the rating'''
    business_data = {}
    business_data = gmapspresence(business)

    business_data["knowledge_base"] = googleknowledgebase(business)
    business_data["vicinity_attention"] = compareRatings(business)
    score = 0
    # get social media if website exists
    if business_data["contacts"]["website"]:
        url = business_data["contacts"]["website"]
        insta = hasInstagram(url)
        fb = hasFacebook(url)
        twitter = hasTwitter(url)
        if insta:
            business_data["contacts"]["instagram"] = insta
            score+=weights['contacts']['instagram']
        print("found insta")
        if fb:
            business_data["contacts"]["facebook"] = fb
            score+=weights['contacts']['facebook']
        print("found fb")
        if twitter:
            business_data["contacts"]["twitter"] = twitter
            score+=weights['contacts']['twitter']
    
    # assign score based on weights
    score += weights['vicinity_attention']*business_data["vicinity_attention"]
    score+=weights['knowledge_base']*business_data['knowledge_base']
    
    print(score)
    return score,business_data

ratings = []

for b in businesses[:1]: # TEMPORARY test on one business
    name = b["name"]
    print(f"Rating {name}...",end=' ')
    rating, details = rate_business(b)
    ratings.append({'name':     name,
                    'rating':   rating,
                    'details':  details})
    print(rating)

# write data to a file
json_string = json.dumps(ratings)
print("Writing data to business_ratings.json... ",end='')
with open('business_ratings.json', 'w') as f:
    f.write(json_string)
print("done")