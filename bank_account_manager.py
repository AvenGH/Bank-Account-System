import os
from bank_account import BankAccount
import account_op
from account_file_handler import AccountFileHandler as afh
from email_handler import EmailHandler as eh

os.system("cls")


class BankAccountManager:

    @classmethod
    def get_accounts(cls):
        cls.cursor.execute("SELECT * FROM accounts")
        accounts = cls.cursor.fetchall()
        return accounts
    

    @classmethod
    def select_account(cls, accno):
        cls.cursor.execute("SELECT * FROM accounts WHERE accno = %s", (accno,))
        return cls.cursor.fetchone()


    @staticmethod
    def create_account():
        age=input("Please Enter Your Age: ")
        if type(eval(age))!=int:
            print("Invalid Age")
            return
        
        if int(age)<18: 
            print("Access Denied! Please Try Again Later")
            return     
        
        try:
            name = input("Enter Account Name: ")
            email = input("Enter Your Email Address: ")
            balance = float(input("Enter Opening Balance: "))
            account = BankAccount(name, email, balance)
            account_op.add_account(account.account_no, account.name, account.balance, account.pin, account.attempts, account.email)
            afh.write_account_details(account)
            eh.send_account_details_email(account)
            print(f"Account For '{name}' Created Successfully. Current Balance: £{account.balance}")
        except Exception as e:
            print("Invalid Details")
            print(e)
            

    @staticmethod
    def log_in():
        print("Please Enter Your Account Number: ")
        account_number=input()
        account_data = account_op.select_account(account_number)
        if not account_data:
            print("Account Not Found!")
            return

        account = BankAccount()
        account.load_from_db(account_number)

        if account.blocked:
            print("Sorry! This account has been blocked")
            return

        print("\nPlease Enter Your PIN:")
        PIN=input()

        if PIN == account.pin:
            BankAccountManager.main_menu(account)
            return

        print("Invalid PIN")
        account_op.update_account(account.account_no, 'attempts', account.attempts - 1)
        account.update()

        if account.attempts>0:
            print("We will lock your account if you continue to enter your details incorrectly")
        
        elif account.attempts==0:
            print("Account Blocked")
            account_op.update_account(account.account_no, 'is_blocked', True)
            
        account.update()
        return     


    @staticmethod
    def exit_program():
        print("Thank You For Banking With Us!")
        quit()


    @staticmethod
    def transfer(account):
        payee_acc_no=input("Enter Payee's Account Number: ")
        account2 = account_op.select_account(payee_acc_no)

        if account2==None:
            print("Account Not Found!")
            return
        
        amount = float(input("Enter transfer amount: "))
        if not isinstance(amount,float):
            return
        
        if amount<0:
            print("Invalid Amount")
            return       
        
        if amount > account.balance:
            print("Insufficient Balance.")
            return
        
        account2 = BankAccount()
        account2.load_from_db(payee_acc_no)

        account_op.update_account(account.account_no, 'balance', account.balance - amount)
        account_op.update_account(account2.account_no, 'balance', account2.balance + amount)
        print(f"Transferred £{amount} Successfully")
        print(f"From: {account.name} To: {account2.name}")
        account.record_transaction("Transfer",amount)
        account2.record_transaction(f"Credit From {account.account_no}",amount)


    @classmethod
    def start_menu(cls):     
        while True:
            start_menu_options={
                '1': cls.create_account,
                '2': cls.log_in,
                '3': cls.exit_program
            }

            print("\nWelcome to Banks4Us Online Banking!")
            print("\n1. Create an account")
            print("2. Log in to an account")
            print("3. Exit")

            choice = input("\nEnter Your Option No. ")
            print()

            if choice in start_menu_options:
                start_menu_options[choice]()
            else:
                print("Oops! Invalid Option...")


    @classmethod
    def main_menu(cls, account):
        main_menu_options={
            '1': account.deposit,
            '2': account.withdraw,
            '3': account.check_balance,
            '4': lambda: cls.transfer(account),
            '5': account.change_PIN,
            '6': account.view_transaction_history,
            '7': cls.start_menu
        }

        while True:
            print("\nMAIN MENU:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transfer")
            print("5. Change PIN")
            print("6. View Transaction History")
            print("7. Exit")

            choice = input("\nEnter Your Option No. ")

            if choice in main_menu_options:
                main_menu_options[choice]()
                account.update()    
            else:
                print("Oops! Invalid Option...")
