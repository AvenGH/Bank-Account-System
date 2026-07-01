import random
from account_file_handler import AccountFileHandler as afh
from utils import generate_account_no
from email_handler import EmailHandler as eh
import account_op
from database import cursor


class BankAccount:
    def __init__(self, name=None, email=None, initial_balance=None):
        self.account_no = generate_account_no()
        self.balance = initial_balance
        self.sort_code = "40-39-13"
        self.pin = str(random.randrange(1000, 10000))
        self.name = name
        self.email = email
        self.attempts = 3
        self.blocked = False
        self.transaction_history = []


    def load_from_db(self, accno):
        account_data = account_op.select_account(accno)
        if account_data:
            (
                self.account_no,
                self.name,
                self.balance,
                self.sort_code,
                self.pin,
                self.attempts,
                self.blocked,
                self.transaction_history,
                self.email
            ) = account_data.values()
    

    def deposit(self):
        amount = float(input("Enter deposit amount: "))
        if not isinstance(amount, float):
            return

        if amount < 0:
            print("Invalid Amount")
            return
        
        account_op.update_account(self.account_no, 'balance', self.balance + amount)
        print(f"Deposited £{amount} Successfully")
        self.record_transaction("Deposit", amount)


    def withdraw(self):
        amount = float(input("Enter withdraw amount: "))
        if not isinstance(amount, float):
            return

        if amount<0:
            print("Invalid Amount")
            return
        
        if amount > self.balance:
            print("Insufficient Balance.")
            return

        account_op.update_account(self.account_no, 'balance', self.balance - amount)
        print(f"Withdrew £{amount} Successfully")
        self.record_transaction("Withdraw",amount)
            

    def check_balance(self):
        print(f"Your Current Balance is: £{self.balance}")
    

    def change_PIN(self):
        def PIN_valid(PIN):
            try:
                int(PIN)
            except:
                return False

            if len(str(PIN))==4:
                return True

        print("Please Enter Your Current PIN")
        PIN=input()

        if self.pin!=PIN:
            print("Invalid PIN")
            return
        
        while True:
            print("Please Enter Your New PIN:")
            new_PIN=input()

            if not PIN_valid(new_PIN):
                print("PIN Must Be Exactly 4 Digits")
                continue            

            print("Please Confirm Your New PIN")
            confirm_PIN=input()
            if new_PIN!=confirm_PIN:
                print("Incorrect PIN")
                continue

            account_op.update_account(self.account_no, 'pin', confirm_PIN)
            print("Successfully Changed PIN")
            afh.write_PIN_confirmation(self)
            eh.send_pin_confirmation_email(self)
            break
                          

    def record_transaction(self,transaction_type,amount):
        transaction = {"name": self.name, "account_number": self.account_no, "transaction_type": transaction_type, "amount": amount, "balance": self.balance}
        self.transaction_history.append(transaction)


    def view_transaction_history(self):
        print("Sorry! This option is currently not available")


    def update_account(self, accno, field, value):
        query = f"UPDATE accounts SET {field} = %s WHERE accno = %s"
        cursor.execute(query, (value, accno))


    def update(self):
        updated_account = account_op.select_account(self.account_no)
        if updated_account:
            (
                self.account_no,
                self.name,
                self.balance,
                self.sort_code,
                self.pin,
                self.attempts,
                self.blocked,
                self.transaction_history,
                self.email
            ) = updated_account.values()

        