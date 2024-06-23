import os

import django
from pymongo import MongoClient

import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hm_10.settings")
django.setup()


from quotes.models import Quote, Tag, Author


client = MongoClient("mongodb://localhost")
db = client.hm


authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname = author["fullname"],
        born_date = author["born_date"],
        born_location = author["born_location"],
        description = author["description"]
    )


quotes = db.quotes.find()


for quote in quotes:
    exist_quote = Quote.objects.filter(quote=quote['quote']).exists()
    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote=quote['quote'],  # Corrected to access the quote field of each document
            author=a
        )
        tags = []
        for tag in quote.get('tags', []):  # Using get method to avoid KeyErrors
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)
        q.tags.add(*tags)
