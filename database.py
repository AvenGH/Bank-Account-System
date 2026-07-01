import psycopg

try:
    connection = psycopg.connect(
        dbname='BankingManagementSystem',
        user="postgres",
        password="password",
        host="localhost",
        port=5432
    )
    connection.autocommit = True
    cursor = connection.cursor(row_factory=psycopg.rows.dict_row)
except psycopg.Error as e:
    print("Something went wrong. Please try again later.", e)



