from collections import UserDict

class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):

    def __init__(self, value):

        super().__init__(value)

        if not value:
            raise ValueError("Enter the correct name")



class Phone(Field):

    def __init__(self, value):

        super().__init__(value)

        if len(value) != 10 or not value.isdigit():
            raise ValueError("Incorrect number format. Enter 10 digits")


class Record():

    def __init__(self, name, phone = None):

        self.name = Name(name)
        self.phones = []

    def __str__(self):

        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):

        self.phones = list(filter(lambda tel: tel.value != phone, self.phones))

    def edit_phone(self, current_phone, new_phone):

        for phone in self.phones:
            if phone.value == current_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number '{current_phone}' not found")

    def find_phone(self, phone):

        found_phone = list(filter(lambda tel: tel.value == phone, self.phones))

        return found_phone[0] if found_phone else None


class AddressBook(UserDict):

    def add_record(self, contact):

        self.data[contact.name.value] = contact

    def find(self, name):

        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):

        if name in self.data:
            self.data.pop(name)


def main():

    book = AddressBook()

if __name__ == "__main__":
    main()



