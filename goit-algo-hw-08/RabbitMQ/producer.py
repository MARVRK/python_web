import pika
import json
from mongoengine import connect
from model import Contact

# Connect to MongoDB
connect('contacts', host='mongodb+srv://marv:marv1@cluster-marv.whuu4ly.mongodb.net/')

# Connect to RabbitMQ
credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='contacts')

# Retrieve existing contacts from MongoDB
existing_contacts = Contact.objects()

for contact in existing_contacts:
    channel.basic_publish(
        exchange='',
        routing_key='contacts',
        body=json.dumps({'contact_id': str(contact.id)})
    )

print("Existing contacts' IDs sent to RabbitMQ")
connection.close()
