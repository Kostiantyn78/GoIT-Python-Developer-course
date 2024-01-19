from bson import ObjectId
import pika

import connect
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


def send_sms(phone_number, message):
    print(f"Sent SMS-message '{message}' to phone_number {phone_number}")


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=ObjectId(contact_id)).first()
    if contact and not contact.message_sent:
        send_sms(contact.phone_number, "Message text.")
        contact.message_sent = True
        contact.save()
        print(f"Message sent for contact {contact.full_name}, contact_id - {contact_id}")


def main():
    channel.basic_consume(queue='contact_ids_sms', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
