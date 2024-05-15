import pickle
from record import Record
from addressbook import AddressBook
from datetime import datetime

def input_error(func):   # Decorator for handling input errors
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return str(e)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command."
        except:
            return "Invalid command."
    return inner

def parse_input(user_input):  # Parse user input into command and arguments
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

def save_data(book, filename="addressbook.pkl"): # Save the addressbook data to a file using pickle serialization.

    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):  # Load the addressbook data from a file using pickle deserialization.
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    

# Functions for handling different commands

@input_error
def add_birthday(args, address_book): # Add a birthday to a contact
    name, birthday_str = args
    try:
        birthday = datetime.strptime(birthday_str, '%d.%m.%Y')
    except ValueError:
        raise ValueError("Invalid birthday format. Please use DD.MM.YYYY.")
    
    record = address_book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found.")

    record.birthday = birthday
    return f"Birthday added for contact '{name}'."

@input_error
def show_birthday(args, address_book): # Show the birthday of a contact
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found.")
    if record.birthday:
        return f"The birthday for contact '{name}' is {record.birthday.strftime('%d.%m.%Y')}."
    else:
        return f"No birthday found for contact '{name}'."
 
@input_error
def birthdays(args, address_book): # Show upcoming birthdays
    upcoming_birthdays = address_book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    else:
        return "\n".join([f"Upcoming birthday for {contact['name']} on {contact['birthday_date']}" for contact in upcoming_birthdays])

@input_error
def add_contact(args, address_book): # Add a contact to the address book
    if len(args) < 2:
        raise ValueError("Give me name and at least one phone number, separated by spaces.")
    name = args[0]
    phones = args[1:]
    record = address_book.find(name)
    if record:
        for phone in phones:
            record.add_phone(phone)
        return f"Phone number(s) added to contact '{name}'."
    else:
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."

@input_error
def change_contact(args, address_book): # Change a contact's phone number
    if len(args) < 2:
        raise ValueError("Please provide both name and new phone number.")
    if len(args) > 2:
        raise ValueError("Please provide the contact name and the new phone number only.")
    name, new_phone = args[0], args[1]
    record = address_book.find(name)

    # Create a dictionary of available phone numbers for the contact
    available_phones = {str(i): phone for i, phone in enumerate(record.phones)}
    print(f"Available phone numbers for contact {name}:")
    for i, phone in available_phones.items():
        print(f"{i}: {phone}")

    try:
        # Prompt user to select the phone number to change
        chosen_phone = input("Enter the number of the phone you want to change: ")
        old_phone = available_phones[chosen_phone].value
        record.remove_phone(old_phone) # Removing the old number
        record.add_phone(new_phone)    # Adding the new number
        return "Contact updated."
    except KeyError:
        return "Invalid phone number. Please enter a valid number."

@input_error
def show_phone(args, address_book):  # Show phone numbers for a contact
    if len(args) == 0: # Check if the user entered an empty command
        return "Please provide the name of the contact or type 'phone <contact_name>'."
    name = args[0]
    record = address_book.find(name)
    if record: 
        phones = record.find_phone()  
        if len(phones) == 1:
            return f"The phone number for contact '{name}' is: {', '.join(phones)}."
        else:
            return f"The phone numbers for contact '{name}' are: {', '.join(phones)}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_all_contacts(address_book):  # Show all contacts in the address book
    if address_book:
        return "\n".join([str(record) for record in address_book.values()])
    else:
        return "No contacts found."

@input_error
def process_input(command, args, address_book):   # Process the user input command
    if command == "hello":
        return "How can I help you?"
    elif command == "add":
        return add_contact(args, address_book)
    elif command == "change":
        return change_contact(args, address_book)
    elif command == "phone":
        return show_phone(args, address_book)
    elif command == "all":
        return show_all_contacts(address_book)
    elif command == "add-birthday":
        return add_birthday(args, address_book)
    elif command == "show-birthday":
        return show_birthday(args, address_book)
    elif command == "birthdays":
        return birthdays(args, address_book)

    else:
        return "Invalid command."

@input_error
def main():   # Main function to run the program and interact with the user
    address_book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(address_book)
            print("Good bye!")
            break
        else:
            print(process_input(command, args, address_book))

if __name__ == "__main__":
    main()

