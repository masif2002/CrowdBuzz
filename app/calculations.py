def add(a, b):
    return a + b

def sub(a: int, b: int):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    
    def deposit(self, amt):
        self.balance += amt
    
    def withdraw(self, amt):
        if amt > self.balance:
            raise Exception("Insufficient funds!")
        self.balance -= amt
    
    def get_balance(self):
        return self.balance