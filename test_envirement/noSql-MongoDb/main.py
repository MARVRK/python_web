from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

client = MongoClient(
    "mongodb+srv://marv:marv1@cluster-marv.whuu4ly.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.book

# result_one = db.cats.insert_one(
#     {
#         "name": "zupa",
#         "age": 3,
#         "features": ["ходить в капці", "дає себе гладити", "рудий"],
#     }
# )

# print(result_one.inserted_id)

# result_many = db.cats.insert_many(
#     [
#         {
#             "name": "Zuza",
#             "age": 2,
#             "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
#         },
#         {
#             "name": "Bobik",
#             "age": 4,
#             "features": ["ходить в лоток", "дає себе гладити", "білий"],
#         },
#     ]
# )
# print(result_many.inserted_ids)


# db = client.book

result = db.cats.find_one({"_id": ObjectId("6633b1614003eead354834cd")})
print(result)

result = db.cats.find({})
for el in result:
    print(el)

db.cats.update_one({"name": "zupa"}, {"$set": {"age": 4}})
result = db.cats.find_one({"name": "zupa"})
print(result)


