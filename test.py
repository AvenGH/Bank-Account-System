import random
import os
import access_data as ad
import email as me
import account_file_handler as afh
from datetime import datetime
from datacomp import is_digit

# Clear console
os.system("cls" if os.name == "nt" else "clear")

# Load accounts
try:
    accounts = ad.loadData('binary', "accounts.dat")
except Exception as e:
    print(f"Error loading data: {e}")
    accounts = []
print(accounts)

class BankAccount:
    def __init__(self, name, initial_balance, email):
        self.account_no = self.generate_account_no()
        self.balance = initial_balance
        self.sort_code = "40-39-13"
        self.PIN = self.generate_PIN()
        self.name = name
        self.email = email
        self.attempts = 3
        self.blocked = False
        self.transaction_history = []

        afh.write_account_details(self)
        self.send_account_details()

    

    def generate_PIN(self):
        return str(random.randrange(1000, 10000))

    def send_account_details(self):
        try:
            file_name = f"Account Details/account{self.account_no}.txt"
            host_email_address = "banks4usorganisation@gmail.com"
            host_password = "qnqrbspxisssfoiy"
            subject = "Account Details"
            data = f"Hi {self.name}, Please find your account details attached"
            me.send_email(file_name, self.email, host_email_address, subject, data, "txt", host_password)
        except Exception as e:
            print(f"Error sending account details: {e}")

    def deposit(self, amount):
        if is_digit(amount) and amount >= 0:
            self.balance += amount
            print(f"Deposited £{amount} successfully")
            self.record_transaction("Deposit", amount)
        else:
            print("Invalid amount")

    def withdraw(self, amount):
        if is_digit(amount) and amount >= 0:
            if amount > self.balance:
                print("Insufficient balance")
            else:
                self.balance -= amount
                print(f"Withdrew £{amount} successfully")
                self.record_transaction("Withdraw", amount)
        else:
            print("Invalid amount")

    def check_balance(self):
        print(f"Your current balance is: £{self.balance}")

    def transfer(self, payee_account, amount):
        if is_digit(amount) and amount >= 0:
            if amount > self.balance:
                print("Insufficient balance")
            else:
                self.balance -= amount
                payee_account.balance += amount
                print(f"Transferred £{amount} successfully")
                print(f"From: {self.name} To: {payee_account.name}")
                self.record_transaction("Transfer", amount)
                payee_account.record_transaction(f"Credit from {self.account_no}", amount)
        else:
            print("Invalid amount")

    def change_PIN(self, current_PIN, new_PIN, confirm_PIN):
        if self.PIN != current_PIN:
            print("Incorrect PIN")
            return

        if not self.is_valid_PIN(new_PIN):
            print("PIN must be exactly 4 digits")
            return

        if new_PIN != confirm_PIN:
            print("PINs do not match")
            return

        self.PIN = new_PIN
        print("Successfully changed PIN")
        afh.write_PIN_confirmation(self)
        self.send_PIN_confirmation()

    def is_valid_PIN(self, PIN):
        return PIN.isdigit() and len(PIN) == 4

    def send_PIN_confirmation(self):
        try:
            file_name = f"PIN Confirmations/account{self.account_no}.txt"
            host_email_address = "banks4usorganisation@gmail.com"
            host_password = "qnqrbspxisssfoiy"
            subject = "PIN Confirmation"
            data = f"Hi {self.name}, Your PIN has been successfully changed"
            me.send_email(file_name, self.email, host_email_address, subject, data, "txt", host_password)
        except Exception as e:
            print(f"Error sending PIN confirmation: {e}")

    def record_transaction(self, transaction_type, amount):
        transaction = {
            "name": self.name,
            "account_number": self.account_no,
            "transaction_type": transaction_type,
            "amount": amount,
            "balance": self.balance
        }
        self.transaction_history.append(transaction)

    def close_account(self, PIN):
        if PIN != self.PIN:
            print("Invalid PIN")
            return False
        accounts.remove(self)
        print("Closed account successfully")
        return True

class BankAccountManager:
    @staticmethod
    def select_account(accno):
        for account in accounts:
            if account.account_no == accno:
                return account
        return None

class Main:
    @staticmethod
    def create_account():
        try:
            age = int(input("Please enter your age: "))
            if age < 18:
                print("Access denied! Please try again later.")
                return

            name = input("Enter account name: ")
            email = input("Enter your email address: ")
            balance = float(input("Enter opening balance: "))
            account = BankAccount(name=name, initial_balance=balance, email=email)
            accounts.append(account)
            print(f"Account for '{name}' created successfully. Current balance: £{balance}")
        except ValueError:
            print("Invalid details")

    @staticmethod
    def log_in():
        account_number = input("Please enter your account number: ")
        account = BankAccountManager.select_account(account_number)

        if not account:
            print("Account not found!")
            return None

        if account.blocked:
            print("Sorry! This account has been blocked")
            return None

        PIN = input("Please enter your PIN: ")
        if PIN != account.PIN:
            print("Invalid PIN")
            account.attempts -= 1
            if account.attempts > 0:
                print("We will lock your account if you continue to enter your details incorrectly")
            if account.attempts == 0:
                print("Account blocked")
                account.blocked = True
            return None
        return account

    @staticmethod
    def exit_program():
        try:
            ad.saveData("accounts.dat", accounts)
        except Exception as e:
            print(f"Error saving data: {e}")
        print("Thank you for banking with us!")
        quit()

    @staticmethod
    def start_menu():
        while True:
            print("\nWelcome to Banks4Us Online Banking!")
            print("\n1. Create an account")
            print("2. Log in to an account")
            print("3. Exit")

            choice = input("\nEnter your option no. ")

            if choice == '1':
                Main.create_account()
            elif choice == '2':
                account = Main.log_in()
                if account:
                    Main.main_menu(account)
            elif choice == '3':
                Main.exit_program()
            else:
                print("Oops! Invalid option...")

    @staticmethod
    def main_menu(account):
        while True:
            print("\nMAIN MENU:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transfer")
            print("5. Change PIN")
            print("6. View Transaction History")
            print("7. Close Account")
            print("8. Exit")

            choice = input("\nEnter your option no. ")

            if choice == '1':
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
            elif choice == '2':
                amount = float(input("Enter withdraw amount: "))
                account.withdraw(amount)
            elif choice == '3':
                account.check_balance()
            elif choice == '4':
                payee_acc_no = input("Enter payee's account number: ")
                payee_account = BankAccountManager.select_account(payee_acc_no)
                if payee_account:
                    amount = float(input("Enter transfer amount: "))
                    account.transfer(payee_account, amount)
                else:
                    print("Account not found!")
            elif choice == '5':
                current_PIN = input("Please enter your current PIN: ")
                new_PIN = input("Please enter your new PIN: ")
                confirm_PIN = input("Please confirm your new PIN: ")
                account.change_PIN(current_PIN, new_PIN, confirm_PIN)
            elif choice == '6':
                for transaction in account.transaction_history:
                    print(transaction)
            elif choice == '7':
                PIN = input("Please enter your PIN: ")
                if account.close_account(PIN):
                    Main.exit_program()
            elif choice == '8':
                Main.exit_program()
            else:
                print("Oops! Invalid option...")

if __name__ == "__main__":
    Main.start_menu()
