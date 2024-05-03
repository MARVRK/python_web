from faker import Faker
from mongoengine import connect
from model import Contact

# Connect to MongoDB
connect('contacts', host='mongodb+srv://marv:marv1@cluster-marv.whuu4ly.mongodb.net/')

fake = Faker()

for _ in range(10): 
    contact = Contact(
        full_name=fake.name(),
        email=fake.email()
    )
    contact.save()

print("Fake contacts generated in MongoDB")
