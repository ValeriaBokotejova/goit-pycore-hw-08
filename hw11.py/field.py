class Field: # Define the base class for fields in a record
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)