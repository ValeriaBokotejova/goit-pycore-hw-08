from name import Name
from phone import Phone
from birthday import Birthday

class Record:  # Class representing a contact record
    def __init__(self, name):
        self.name = Name(name) # Store the contact name
        self.phones = []       # Initialize an empty list for phone numbers
        self.birthday = None

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            raise ValueError("Invalid birthday format.")
        self.birthday = birthday

    def add_phone(self, phone):  # Add a phone number to the list
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):  # Remove a phone number from the list
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):   # Edit a phone number in the list
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone=None):  # Find a phone number in the list
        if phone is None:
            return [p.value for p in self.phones]
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise ValueError("Phone number not found")
    
    def __str__(self):   # String representation of the record
        # Determine the number of phones
        num_phones = len(self.phones)
        phone_word = "phone" if num_phones == 1 else "phones"
        # Construct the string representation
        return f"Contact name: {self.name.value}, {phone_word}: {', '.join(str(p) for p in self.phones)}"