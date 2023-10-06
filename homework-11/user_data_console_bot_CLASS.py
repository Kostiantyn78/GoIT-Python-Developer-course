from collections import UserDict
from datetime import datetime

class Field:

    def __init__(self, value):

        self._value = None
        self.value = value

    @property
    def value(self):

        return self._value

    @value.setter
    def value(self, value):

        self._value = value

    def __str__(self):

        return str(self.value)


class Name(Field):

    @Field.value.setter
    def value(self, value):

        if not value:
            raise ValueError("Enter the correct name")
        else:
            self._value = value


class Phone(Field):

    @Field.value.setter
    def value(self, value):

        if len(value) != 10 or not value.isdigit():
            raise ValueError("Incorrect number format. Enter 10 digits")
        else:
            self._value = value


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
    
        if value:
            self._value = datetime.strptime(value[0], '%d/%m/%Y').date()


class Record():

    def __init__(self, name, phone=None, birthday=None):

        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):

        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_phone(self, phone):

        self.phones.append(phone)

    def remove_phone(self, phone):

        self.phones = list(filter(lambda tel: tel.value != phone, self.phones))

    def edit_phone(self, current_phone, new_phone):

        for phone in self.phones:
            if phone.value == current_phone:
                phone.value = new_phone
                return
        raise ValueError

    def find_phone(self, phone):

        found_phone = list(filter(lambda tel: tel.value == phone, self.phones))

        return found_phone[0] if found_phone else None

    def add_birthday(self, birthday):

        self.birthday = Birthday(birthday)

    def days_to_birthday(self):

        if self.birthday.value:

            today = datetime.now().date()
            current_birthday = self.birthday.value.replace(year=today.year)

            if current_birthday < today:
                current_birthday = current_birthday.replace(year=today.year + 1)

            return (current_birthday - today).days
        else:
            return None

class AddressBook(UserDict):

    def add_record(self, contact):

        self.data[contact.name.value] = contact

    def find(self, name):

        if str(name) in self.data:
            return True
        else:
            return False

    def delete(self, name):

        self.data.pop(str(name))

    def iterator(self, qty_of_records):

        set_of_records = {}
        n = 0

        for name, record in self.data.items():
            set_of_records[name] = record
            n += 1

            if n == qty_of_records:
                yield set_of_records
                set_of_records = {}
                n = 0

        if set_of_records:
            yield set_of_records


def input_error(func):
    def inner(*args, **kwargs):
        try:
            rezult = func(*args, **kwargs)
            return rezult, None
        except KeyError:
            return None, 'Error: contact not found.'
        except (ValueError, IndexError, TypeError):
            return None, "Error: Invalid data. Please enter correct contact data."
    return inner

def user_text_parser(text_from_user, COMMANDS):

    parsed_text = text_from_user.lower().strip().split()

    command = ''
    error = ''
    contact_data  = []

    if not parsed_text:
        error = 'Invalid command ! Try again.'
    elif len(parsed_text) > 1 and f'{parsed_text[0]} {parsed_text[1]}' in COMMANDS.keys():
        command = f'{parsed_text[0]} {parsed_text[1]}'
        contact_data = parsed_text[2:]
    elif parsed_text[0] in COMMANDS.keys():
        command = parsed_text[0]
        contact_data = parsed_text[1:]
    else:
        error = 'Invalid command ! Try again.'

    return error, command, contact_data
@input_error
def greeting(*args):

    return 'How can I help you ?'
@input_error
def end_work(*args):

    return 'Good bye !'
@input_error
def add_phone(contact_data, book):

    if book.find(contact_data[0]):

        if book[contact_data[0]].find_phone(contact_data[1]) is None:

            book[contact_data[0]].add_phone(Phone(contact_data[1]))
    else:

        record = Record(contact_data[0])
        record.add_phone(Phone(contact_data[1]))
        book.add_record(record)

    return f'Phone number {contact_data[1]} added for contact" {contact_data[0]}"'

@input_error
def del_contact(contact_data, book):

    contact = book.data[contact_data[0]]
    book.delete(contact.name)

    return f'Contact "{contact.name}" deleted'


@input_error
def show_all(contact_data, book: AddressBook):

    qty_of_records = 5

    for records in book.iterator(qty_of_records):

        for name, record in records.items():
            print(record)

    return f'Printed {len(book)} contacts'

@input_error
def get_phone(contact_data, book):

    return book.data[contact_data[0]]

@input_error
def change_phone(contact_data, book):

    book[contact_data[0]].edit_phone(contact_data[1], contact_data[2])

    return f'Phone number {contact_data[1]} of the contact "{contact_data[0]}" was changed for the number {contact_data[2]}'

@input_error
def erase_number(contact_data, book: AddressBook):

    if book[contact_data[0]].find_phone(contact_data[1]):
        book[contact_data[0]].remove_phone(contact_data[1])
    else:
        raise ValueError

    return f'Phone number {contact_data[1]} of the contact "{contact_data[0]}" was erased'

@input_error
def set_birthday(contact_data, book: AddressBook):

    record = book.data[contact_data[0]]
    record.add_birthday(contact_data[1:])

    return f'Birthday for contact "{contact_data[0]}" added'

@input_error
def when_birthday(contact_data, book: AddressBook):

    days_to_birthday = book.data[contact_data[0]].days_to_birthday()

    if days_to_birthday:
        return f'Contact "{contact_data[0]}" birthday is in {days_to_birthday} days'
    else:
        return f'Birthday for contact "{contact_data[0]}" has not been set yet'

def main():

    book = AddressBook()

    print('''Hello ! 
    I`m your Command Line Interface helper. 
    I can to work with your phone book:
    - store name and phone number;
    - find a phone number by name;
    - change the recorded phone number;
    - display all records in the console.
        
        available commands:
    - add <name> <phone number>
    - del <name>
    - change <name> <phone number> <new phone number>
    - phone <name>
    - show all
    - good bye, close, exit -> EXIT
    - set birthday <name> <dd/mm/yyyy>
    - erase_number <name> <phone number>    
            ''')

    COMMANDS = {
        'hello': greeting,
        'good bye': end_work,
        'close': end_work,
        'exit': end_work,
        'add': add_phone,
        'show all': show_all,
        'phone': get_phone,
        'change': change_phone,
        'set birthday': set_birthday,
        'when birthday': when_birthday,
        'del': del_contact,
        'erase number': erase_number
    }

    while True:

        text_from_user = input('Input your command - ')
        parsing_text_error, command, contact_data = user_text_parser(text_from_user, COMMANDS)

        if not parsing_text_error:

            rezult, command_error = COMMANDS[command](contact_data, book)

            if not command_error:

                match command:

                    case 'exit' | 'close' | 'good bye':
                        print(rezult)
                        break

                print(rezult)

            else:
                print(command_error)
        else:
            print(parsing_text_error)

if __name__ == '__main__':
    main()