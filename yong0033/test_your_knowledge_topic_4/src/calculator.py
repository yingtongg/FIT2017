# Student name: Ong Ying Tong
# Student ID: 34477306

class Calculator(object):
    def __init__(self):
        self.answer = 0

    def get_answer(self):
        return self.answer
    
    def add(self, value):
        self.answer += value
        return self   # allow chaining

    def subtract(self, value):
        self.answer -= value
        return self   # allow chaining

    def multiply(self, value):
        self.answer *= value
        return self   # allow chaining

    def divide(self, value):
        if value == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.answer /= value
        return self   # allow chaining
