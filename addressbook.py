from collections import UserDict
from datetime import datetime

class AddressBook(UserDict):  # Class for managing the address book
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = [] 

        for record in self.values():
            if record.birthday:
                birthday_date = record.birthday.date()
                birthday_this_year = birthday_date.replace(year=today.year) # Set the birthday to this year
                if birthday_this_year < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)  # If birthday already passed this year, set to next year
                else:
                    birthday_date = birthday_this_year
                days_until_birthday = (birthday_date - today).days
                if 0 <= days_until_birthday <= 7:  # Check if the birthday is within the next week
                    upcoming_birthdays.append({"name": record.name, "birthday_date": birthday_date.strftime("%d.%m.%Y")})
        return upcoming_birthdays

    def add_record(self, record):    # Add a record to the address book
        self.data[record.name.value] = record

    def find(self, name):   # Find a record in the address book by name
        return self.data.get(name)

    def delete(self, name): # Delete a record from the address book by name
        del self.data[name]