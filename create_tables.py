import sqlite3

connection = sqlite3.connect('bank.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, password TEXT, first_name TEXT, last_name TEXT, date_of_birth TEXT, address TEXT, contact_number INTEGER, email TEXT, occupation TEXT)')
cursor.execute('CREATE TABLE savings_accounts (account_number INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, balance REAL, open_date TEXT, status TEXT)')
cursor.execute('CREATE TABLE transfers (transfer_id INTEGER PRIMARY KEY AUTOINCREMENT, account_number INTEGER, transfer_type TEXT, amount REAL, date TEXT, time TEXT)')
cursor.execute('CREATE TABLE messages (message_id INTEGER PRIMARY KEY AUTOINCREMENT, receiver_id INTEGER, message_content TEXT, date TEXT, time TEXT)')
cursor.execute('CREATE TABLE loans (loan_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, loan_type TEXT, loan_amount REAL, interest_rate REAL, term INTEGER, start_date TEXT, end_date TEXT, status TEXT)')

connection.commit()

cursor.close()
connection.close()