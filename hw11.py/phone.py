from field import Field

class Phone(Field): # Class for storing and validating phone numbers
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10: 
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)