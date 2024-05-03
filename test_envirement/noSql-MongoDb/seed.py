from models import Notes, Record, Tag
import connect

# спочатку - створити об'єкт Tag
# tag = Tag(name='Purchases')
# # потім - створення об'єктів Record
# record1 = Record(description='Buying sausage')
# record2 = Record(description='Buying milk')
# record3 = Record(description='Buying oil')
# #  Останнє - створюємо об'єкт Note і зберігаємо його
# Notes(name='Shopping', records=[record1, record2, record3], tags=[tag, ]).save()

# Notes(name='Going to the movies', records=[Record(description='Went to see the Avengers'), ], tags=[Tag(name='Fun'), ]).save()

notes = Notes.objects()
print("-------------------")
for note in notes:
    print(note.to_mongo().to_dict())

notes = Notes.objects()
for note in notes:
    print("-------------------")
    records = [f'description: {record.description}, done: {record.done}' for record in note.records]
    tags = [tag.name for tag in note.tags]
    print(f"id: {note.id} name: {note.name} date: {note.created} records: {records} tags: {tags}")
