import random


class Account:

    def __init__(self, number):
        self.number = number
        self.pin = self.generate_pin()
        self.balance = 0

    # custom method
    @staticmethod
    def generate_pin():
        pin_ = ""
        for _ in range(4):
            pin_ += str(random.choice(range(0, 10)))
        return pin_

    def add_deposit(self, value):
        self.balance += value

    def get_balance(self):
        return self.balance
