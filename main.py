import json

with open("input-alt.json", 'r') as f:
    contents = f.read()

businesses = json.loads(contents)

def rate_business(business):
    
    return 5., {}

ratings = {}

for b in businesses:
    name = b["name"]
    print(f"Rating {name}...",end=' ')
    rating, details = rate_business(b)
    ratings[name] = {'rating': rating,
                     'details': details}
    print(rating)