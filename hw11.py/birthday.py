from datetime import datetime
from field import Field

class Birthday(Field): # Class for storing and validating birthdays.
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
            self.value = date_obj
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")