# Write your code here
import random
import sqlite3

from account import Account


def create_table(dbname_, query_):
    try:
        connection = sqlite3.connect(dbname_)
        cursor = connection.cursor()
        cursor.execute(query_)
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Error - ", error)
    finally:
        if (connection):
            connection.close()
    return None


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
        acc_ = Account(card_number)
        accounts.update({card_number: acc_})
        save_acc(acc_)
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
    load_acc(card_number_, pin_)
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
    print(list(cursor_.fetchone()))
    cursor_.close()


card_numbers = []
accounts = {}

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
        break
