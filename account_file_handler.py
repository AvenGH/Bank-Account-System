class AccountFileHandler:
    email = "pytrustbankltd619@gmail.com"

    @classmethod
    def write_account_details(cls, account):
        with open(f"Account Details\\account{account.account_no}.txt","w") as myfile:
            myfile.write(
            f"""
        Dear {account.name},

        Your account has successfully been created.

        Your Default PIN Is: {account.pin}
        Your Account Number Is: {account.account_no}
        Your Sort Code Is: {account.sort_code}

        Your Opening Balance Is: £{account.balance:.02f}

        Any other queries, please contact us on {cls.email}

            """)

    @classmethod
    def write_PIN_confirmation(cls, account):
        with open(f"PIN Confirmations\\account{account.account_no}.txt","w") as myfile:
            myfile.write(
            f"""
        Dear {account.name}, [{account.account_no}]

        Your New PIN Is: {account.pin}

        Any other queries, please contact us on {cls.email}

            """)
