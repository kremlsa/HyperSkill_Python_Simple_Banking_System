# Write your code here
import random
import sqlite3

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
    while True:
        card_number = generate_card_number()
        if check_number(card_number):
            continue
        acc_ = Account(card_number)
        save_acc(acc_)
        print("Your card has been created")
        print("Your card number:")
        print(acc_.number)
        print("Your card PIN:")
        print(acc_.pin)
        print()
        break


def log_into_account():
    print("Enter your card number:")
    card_number_ = input()
    print("Enter your PIN:")
    pin_ = input()
    print()
    acc_ = load_acc(card_number_, pin_)
    if acc_:
        account_menu(list(acc_))
    else:
        print("Wrong card number or PIN!")
    print()


def account_menu(acc_):
    print("You have successfully logged in!")
    print()
    while True:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice_ = input()
        print()
        if choice_ == "1":
            print("Balance: {}".format(get_balance(acc_[1])))
            print()
        elif choice_ == "2":
            print("Enter income:")
            income_ = input()
            add_income(acc_[1], income_)
        elif choice_ == "3":
            make_transfer(acc_[1])
        elif choice_ == "4":
            del_account(acc_[1])
            break
        elif choice_ == "5":
            break
        elif choice_ == "0":
            print("Bye!")
            exit(0)
    print()


def del_account(num_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("DELETE FROM card WHERE number = {}".format(num_))
    connection_.commit()
    cursor_.close()
    print("The account has been closed!")
    print()


def make_transfer(num_):
    print("Transfer")
    print("Enter card number:")
    target_num_ = input()

    if int(calculate_luhn(target_num_[:len(target_num_) -1])) != int(target_num_[-1]):
        print("Probably you made a mistake in the card number. Please try again!")
        return
    if check_number(target_num_) is None:
        print("Such a card does not exist.")
        print()
        return
    print("Enter how much money you want to transfer:")
    value_ = input()
    if get_balance(num_) < int(value_):
        print("Not enough money!")
        print()
        return
    rem_income(num_, value_)
    add_income(target_num_, value_)
    print("Success!")
    print()


def check_number(num_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("SELECT * FROM card WHERE number={}".format(num_))
    result_ = cursor_.fetchone()
    cursor_.close()
    return result_


def get_balance(num_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("SELECT balance FROM card WHERE number={}".format(num_))
    result_ = cursor_.fetchone()
    cursor_.close()
    return int(result_[0])


def add_income(num_, value_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("UPDATE card SET balance=balance+{} WHERE number={}".format(value_, num_))
    connection_.commit()
    cursor_.close()
    print("Income was added!")
    print()


def rem_income(num_, value_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("UPDATE card SET balance=balance-{} WHERE number={}".format(value_, num_))
    connection_.commit()
    cursor_.close()
    print("Income was added!")
    print()


def save_acc(account_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("""INSERT INTO card (number, pin, balance)
                  VALUES ({}, {}, {})""".format(account_.number, account_.pin, account_.balance))
    connection_.commit()
    cursor_.close()


def load_acc(number_, pin_):
    connection_ = sqlite3.connect("card.s3db")
    cursor_ = connection_.cursor()
    cursor_.execute("SELECT * FROM card WHERE number={} and pin={}".format(number_, pin_))
    result_ = cursor_.fetchone()
    cursor_.close()
    return result_


connection = sqlite3.connect("card.s3db")
cursor = connection.cursor()
create_table_query = """CREATE TABLE IF NOT EXISTS card (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            number TEXT NOT NULL UNIQUE,
                            pin text NOT NULL,
                            balance INTEGER);"""
cursor.execute(create_table_query)
connection.commit()
cursor.close()

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
        print("Bye!")
        break
