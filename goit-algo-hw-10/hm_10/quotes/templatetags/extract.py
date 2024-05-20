from django import template
from bson.objectid import ObjectId
from ..utils import get_mongodb

register = template.Library()


def get_author(_id):
    db = get_mongodb()
    author =  author = db.authors.find_one({'_id': ObjectId(_id)})
    return author["fullname"]


register.filter('author', get_author )

