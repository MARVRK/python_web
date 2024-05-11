from datetime import datetime
from mongoengine import  Document, CASCADE
from connect import connect_to_database
from mongoengine.fields import ReferenceField, ListField, StringField, DateField

connect_to_database()

class Author(Document):
    full_name = StringField(required = True, unique = True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quotes(Document):
    tags = ListField(StringField(max_length=100))
    author = ReferenceField(Author, reverse_delete_rule = CASCADE)
    quote = StringField()
    creted = DateField(default=datetime.now())
    meta = {"collection": "quotes"}
