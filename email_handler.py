import email_operations as eo

class EmailHandler:
    host_email_address = "pytrustbankltd619@gmail.com"
    host_password = "ruoh vrak aiou qcqg"

    @classmethod
    def send_account_details_email(cls, account):
        with open(f"Account Details\\account{account.account_no}.txt","rb") as myfile:
            file_name=myfile.name
            subject="Account Details"
            data=f"Hi {account.name}, Please find your account details attached:"
            subtype="txt"
            eo.send_email(
                file_name, cls.host_email_address, account.email, subject, data, subtype, cls.host_password
            )

    @classmethod
    def send_pin_confirmation_email(cls, account):
        with open(f"PIN Confirmations\\account{account.account_no}.txt","rb") as myfile:
            file_name=myfile.name
            subject="PIN confirmation"
            data=f"Hi {account.name}, Your PIN has successfully been changed"
            subtype="txt"
            eo.send_email(
                file_name, cls.host_email_address, account.email, subject, data, subtype, cls.host_password
            )