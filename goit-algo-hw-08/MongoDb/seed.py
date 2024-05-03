from main import Author, Quotes
import json
from mongoengine import NotUniqueError


if __name__ == "__main__":

        with open ('authors.json', encoding= "utf-8") as fd:
            data = json.load(fd)
        try:
            for e in data:
                    author = Author(full_name = e.get("fullname"), born_date = e.get("born_date"), 
                    born_location= e.get("born_location"), description = e.get("description"))
                    author.save()
        except NotUniqueError:
            print(f"Author {e.get("fullname")} already exists")

        with open ('quotes.json', encoding= "utf-8") as fd:
            data = json.load(fd)
            quotes = []
            for e in data:
                author, *_ = Author.objects(full_name = e.get("author"))
                quotes = Quotes(quote = e.get("quote"), tags = e.get("tags"))
                quotes.save()


                
            