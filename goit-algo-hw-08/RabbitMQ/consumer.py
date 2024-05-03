import pika
import json
from model import Contact
from mongoengine import connect

connect('contacts', host='mongodb+srv://marv:marv1@cluster-marv.whuu4ly.mongodb.net/')

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='contacts')

def callback(ch, method, properties, body):
    contact_id = json.loads(body)['contact_id']
    contact = Contact.objects(id=contact_id).first()

    send_email(contact)

    contact.message_sent = True
    contact.save()

    print(f"Email sent to {contact.email}")

def send_email(contact):
    print(f"Simulating email to {contact.email}")

# Set up consumer to receive messages from RabbitMQ
channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
