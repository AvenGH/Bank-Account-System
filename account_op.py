#SQL Functions for adding, displaying, modifying and deleting accounts

from database import cursor


def get_accounts():
    cursor.execute("SELECT * FROM accounts")
    return cursor.fetchall()

def select_account(accno):
    cursor.execute("SELECT * FROM accounts WHERE accno = %s", (accno,))
    return cursor.fetchone()

def add_account(accno, name, balance, PIN, attempts, email):
    cursor.execute(
        "INSERT INTO accounts (accno, name, balance, pin, sort_code, attempts, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (accno, name, balance, PIN, "40-39-13", attempts, email)
    )

def remove_account(accno):
    cursor.execute("DELETE FROM accounts WHERE accno = %s", (accno,))

def update_account(accno, field, value):
    query = f"UPDATE accounts SET {field} = %s WHERE accno = %s"
    cursor.execute(query, (value, accno))

def update(account):
    updated_account = select_account(account['accno'])
    if updated_account:
        account.update(updated_account)


# TESTING AREA:
#--------------------------------------------

#type a command...

