from field import Field

class Name(Field): # Class for storing and validating contact names
    def __init__(self, value):
        value = value.lower()   # Convert all letters to lowercase
        if not value.isalpha():  # Check if the name contains only alphabetic characters
            raise ValueError("Name must contain only alphabetic characters.")
        super().__init__(value)