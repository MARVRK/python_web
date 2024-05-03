from connect import connect_to_database
from main import Author, Quotes

def find_by_author(name):
    author = Author.objects(name=name).first()
    if author:
        quotes = Quotes.objects(author=author)
        return [quote.quote for quote in quotes]
    else:
        return []

def find_by_tag(tag):
    quotes = Quotes.objects(tags=tag)
    return [quote.quote for quote in quotes]

def find_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quotes.objects(tags__in=tags_list)
    return [quote.quote for quote in quotes]

if __name__ == "__main__":
# Connect to MongoDB Atlas
    connect_to_database()

    while True:
        commands = input("Enter command (name: author_name, tag: tag_name, tags: tag1,tag2,..., exit to quit): ").split(': ')
        if commands[0] == "name":
            quotes = find_by_author(commands[1].strip())
            print('\n' .join(quotes))
        elif commands[0] == "tag":
            quotes = find_by_tag(commands[1].strip())
            print('\n' .join(quotes))
        elif commands[0] == "tags":
            quotes = find_by_tags(commands[1].strip())
            print('\n' .join(quotes))
        elif commands[0] == "exit":
            break