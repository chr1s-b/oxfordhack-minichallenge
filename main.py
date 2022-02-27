import json
from tests import *

with open("input-alt.json", 'r') as f:
    contents = f.read()

businesses = json.loads(contents)

def rate_business(business):
    '''Given a name and address of a business, returns a rating between 0.0 and 10.0 and the details that compose the rating'''
    gmaps_score, gmaps_data = gmapspresence(business)

    return 5., {}

ratings = {}

for b in businesses[:1]: # TEMPORARY test on one business
    name = b["name"]
    print(f"Rating {name}...",end=' ')
    rating, details = rate_business(b)
    ratings[name] = {'rating': rating,
                     'details': details}
    print(rating)

# write data to a file
json_string = json.dumps(ratings)
print("Writing data to business_ratings.json... ",end='')
with open('business_ratings.json', 'w') as f:
    f.write(json_string)
print("done")