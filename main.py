import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

print(f"Loaded api key {API_KEY}")

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