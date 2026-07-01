import random
import account_op

accounts = account_op.get_accounts()

def generate_account_no():
    existing_account_numbers = [account['accno'] for account in accounts]
    while True:
        acc_no = str(random.randrange(10000000, 100000000))
        if acc_no not in existing_account_numbers:
            return acc_no
        
