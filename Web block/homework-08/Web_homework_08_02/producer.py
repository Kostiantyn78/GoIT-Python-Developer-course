from faker import Faker
import pika

import connect
from models import Contact

fake = Faker()


def create_contact(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        contact_data = {
            'full_name': fake.name(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'preferred_contact_method': fake.random_element(elements=('email', 'sms'))
        }
        contacts.append(contact_data)
    return contacts


def save_contacts_to_db(contacts_data):
    for contact in contacts_data:
        Contact(**contact).save()


def send_contact_ids_to_queue(contacts):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='contact_ids')

    for contact in contacts:
        contact_id = str(Contact.objects.get(full_name=contact['full_name']).id)
        channel.basic_publish(exchange='', routing_key='contact_ids', body=contact_id)

    connection.close()

if __name__ == '__main__':

    contacts = create_contact(num_contacts = 5)
    save_contacts_to_db(contacts)
    send_contact_ids_to_queue(contacts)
