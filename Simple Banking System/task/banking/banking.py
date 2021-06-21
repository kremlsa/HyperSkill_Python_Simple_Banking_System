# Write your code here
import random
from account import Account


def calculate_luhn(number_):
    temp_ = [int(i) for i in number_]
    for _ in range(len(temp_)):
        if _ % 2 != 1:
            temp_[_] = temp_[_] * 2
    for _ in range(len(temp_)):
        if temp_[_] > 9:
            temp_[_] = temp_[_] - 9
    return abs(sum(temp_) % 10 - 10) % 10


def generate_card_number():
    num_ = "400000"
    for _ in range(9):
        num_ += str(random.choice(range(0, 10)))
    num_ += str(calculate_luhn(num_))
    return num_


def create_account():
    global accounts, card_numbers
    while True:
        card_number = generate_card_number()
        if card_number in card_numbers:
            continue
        card_numbers.append(card_number)
        accounts.update({card_number: Account(card_number)})
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(accounts[card_number].pin)
        print()
        break


def log_into_account():
    print("Enter your card number:")
    card_number_ = input()
    print("Enter your PIN:")
    pin_ = input()
    print()
    if card_number_ in card_numbers and pin_ == accounts[card_number_].pin:
        account_menu(card_number_)
    else:
        print("Wrong card number or PIN!")
    print()


def account_menu(card_number_):
    print()
    print("You have successfully logged in!")
    print()
    while True:
        print("1. Balance")
        print("2. Log out")
        print("0. Exit")
        choice_ = input()
        print()
        if choice_ == "1":
            print("Balance: {}".format(accounts[card_number_].balance))
        elif choice_ == "2":
            break
        elif choice_ == "0":
            exit(0)
    print()


card_numbers = []
accounts = {}

while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice = input()
    print()
    if choice == "1":
        create_account()
    elif choice == "2":
        log_into_account()
    elif choice == "0":
        break
