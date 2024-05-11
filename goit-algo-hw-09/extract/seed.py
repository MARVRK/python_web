import json
from mongoengine import NotUniqueError
from main import Author, Quotes

if __name__ == "__main__":
    with open('authors.json', encoding="utf-8") as fd:
        author_data = json.load(fd)
    try:
        for author_entry in author_data:
            author = Author(
                full_name=author_entry.get("fullname"),
born_date=author_entry.get("born_date"),
                born_location=author_entry.get("born_location"),
                description=author_entry.get("description")
            )
            author.save()
    except NotUniqueError: 
        print(f"Author {author_entry.get('fullname')} already exists")


    with open('quotes.json', encoding="utf-8") as fd:
        quote_data = json.load(fd)
    for quote_entry in quote_data:
        author_name = quote_entry.get("author")[0]  
        author = Author.objects(full_name=author_name).first()  
        quote = Quotes(
                quote=quote_entry.get("quote"),
                tags=quote_entry.get("tags"),
                author=author
            )
        quote.save()  # Save the quote to the database
    else:
            print(f"Author {author_name} not found in the database")
