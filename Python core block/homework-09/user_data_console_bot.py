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

def user_text_parcer(text_from_user, COMMANDS):

    parsed_text = text_from_user.lower().strip().split()

    command = []
    error = ''
    contact_data  = []

    if not parsed_text:
        error = 'Invalid command ! Try again.'
    elif len(parsed_text) > 1 and f'{parsed_text[0]} {parsed_text[1]}' in COMMANDS.keys():
        command = f'{parsed_text[0]} {parsed_text[1]}'
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
def add_contact(phone_book, contact_data):

    phone_book[contact_data[0]] = contact_data[1]
    return phone_book
@input_error
def show_all(phone_book, contact_data):

    for name, phone_number in phone_book.items():
        print(name, phone_number)

    return phone_book
@input_error
def get_phone(phone_book, contact_data):

    return phone_book[contact_data[0]]
@input_error
def change_phone(phone_book, contact_data):

    phone_book[contact_data[0]]
    phone_book[contact_data[0]] = contact_data[1]

    return phone_book

def main():

    print('''Hello ! 
    I`m your Command Line Interface helper. 
    I can to work with your phone book:
    - store name and phone number;
    - find a phone number by name;
    - change the recorded phone number;
    - display all records in the console.
        
        available commands:
    - add <name> <phone number>
    - change <name> <phone number> -> new number
    - phone <name>
    - show all
    - good bye, close, exit -> EXIT    
            ''')
    phone_book = {}

    COMMANDS = {
        'hello': greeting,
        'good bye': end_work,
        'close': end_work,
        'exit': end_work,
        'add': add_contact,
        'show all': show_all,
        'phone': get_phone,
        'change': change_phone,
    }

    while True:

        text_from_user = input('Input your command - ')
        parcing_text_error, command, contact_data = user_text_parcer(text_from_user, COMMANDS)

        if not parcing_text_error:

            rezult, command_error = COMMANDS[command](phone_book, contact_data)

            if not command_error:

                match command:
                    case 'hello' | 'phone':
                        print(rezult)
                    case 'exit' | 'close' | 'good bye':
                        print(rezult)
                        break
                    case 'add':
                        print('Contact added')
                        phone_book = rezult
                    case 'show all':
                        if rezult == {}:
                            print('Phone book is empty')
                    case 'change':
                        print(f'Phone number of contact {contact_data[0].capitalize()} changed successfully')
                        phone_book = rezult

            else:
                print(command_error)
        else:
            print(parcing_text_error)


if __name__ == '__main__':
    main()