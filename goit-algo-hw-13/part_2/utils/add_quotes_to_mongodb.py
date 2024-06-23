import json
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost")
db = client.hm

with open("quotes.json", 'r', encoding="utf-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    author_name = quote['author'][0]  # Extracting the author's name from the list
    author = db.authors.find_one({'fullname': author_name})
    if author:
        try:
            db.quotes.insert_one({
                'quote': quote["quote"],
                'tags': quote["tags"],
                'author': ObjectId(author['_id']),
            })
            print("Quote inserted successfully!")
        except Exception as e:
            print("Error inserting quote:", e)

