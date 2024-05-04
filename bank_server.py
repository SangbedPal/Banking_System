import sqlite3
import socket
import threading
from datetime import datetime

BANK_SERVER_ADDRESS = ('localhost', 8080)
MINIMUM_BALANCE = 1000

def serve_client(client_socket):
    verify_client(client_socket)

    service = client_socket.recv(1024).decode('utf-8')

    if(service == 'Check balance'):
        check_balance(client_socket)
    elif(service == 'Transfer money'):
        transfer_money(client_socket)

def verify_client(client_socket):
    verification_credentials = client_socket.recv(1024).decode('utf-8')

    verification_credentials_list = verification_credentials.split()
    customer_id = int(verification_credentials_list[0])
    password = verification_credentials_list[1]

    connection = sqlite3.connect('bank.db')
    cursor = connection.cursor()

    cursor.execute('SELECT customer_id, password FROM customers')
    customer_credentials_list = cursor.fetchall()

    connection.commit()

    cursor.close()
    connection.close()

    verification_result = 'Incorrect'

    for customer_credentials in customer_credentials_list:
        if(customer_credentials[0] == customer_id):
            if(customer_credentials[1] == password):
                verification_result = 'Correct'
            
            break
            
    client_socket.send(verification_result.encode('utf-8'))

def check_balance(client_socket):
    account_number = int(client_socket.recv(1024).decode('utf-8'))

    connection = sqlite3.connect('bank.db')
    cursor = connection.cursor()

    cursor.execute(f'SELECT balance FROM savings_accounts WHERE account_number={account_number}')
    balance = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    client_socket.send(str(balance).encode('utf-8'))

def transfer_money(client_socket):
    money_transfer_information = client_socket.recv(1024).decode('utf-8')
    
    money_transfer_information_list = money_transfer_information.split()
    sender_account_number = int(money_transfer_information_list[0])
    receiver_account_number = int(money_transfer_information_list[1])
    transfer_amount = float(money_transfer_information_list[2])

    connection = sqlite3.connect('bank.db')
    cursor = connection.cursor()

    cursor.execute(f'SELECT customer_id, balance FROM savings_accounts WHERE account_number = {sender_account_number}')
    sender_id_and_sender_current_balance = cursor.fetchone()

    sender_id = sender_id_and_sender_current_balance[0]
    sender_current_balance = sender_id_and_sender_current_balance[1]

    cursor.execute(f'SELECT customer_id, balance FROM savings_accounts WHERE account_number = {receiver_account_number}')
    receiver_id_and_receiver_current_balance = cursor.fetchone()

    receiver_id = receiver_id_and_receiver_current_balance[0]
    receiver_current_balance = receiver_id_and_receiver_current_balance[1]

    if(transfer_amount > sender_current_balance):
        client_socket.send('Unsuccessful(1)'.encode('utf-8'))
    elif((sender_current_balance - transfer_amount) < MINIMUM_BALANCE):
        client_socket.send('Unsuccessful(2)'.encode('utf-8'))
    else:
        sender_updated_balance = sender_current_balance - transfer_amount
        receiver_updated_balance = receiver_current_balance + transfer_amount

        cursor.execute(f'UPDATE savings_accounts SET balance = {sender_updated_balance} WHERE account_number = {sender_account_number}')
        cursor.execute(f'UPDATE savings_accounts SET balance = {receiver_updated_balance} WHERE account_number = {receiver_account_number}')

        date = str(datetime.now().date())
        time = datetime.now().time().strftime('%H:%M')

        cursor.execute('INSERT INTO transfers (account_number, transfer_type, amount, date, time) VALUES (?, ?, ?, ?, ?)', (sender_account_number, 'Debit', transfer_amount, date, time))
        cursor.execute('INSERT INTO transfers (account_number, transfer_type, amount, date, time) VALUES (?, ?, ?, ?, ?)', (receiver_account_number, 'Credit', transfer_amount, date, time))

        cursor.execute('INSERT INTO messages (receiver_id, message_content, date, time) VALUES (?, ?, ?, ?)', (sender_id, f'Dear customer, RS {transfer_amount} has been debited from your account {sender_account_number}.', date, time))
        cursor.execute('INSERT INTO messages (receiver_id, message_content, date, time) VALUES (?, ?, ?, ?)', (receiver_id, f'Dear customer, your account {receiver_account_number} has been credited with RS {transfer_amount}.', date, time))

        connection.commit()

        cursor.close()
        connection.close()

        client_socket.send('Successful'.encode('utf-8'))
        
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(BANK_SERVER_ADDRESS)
    server_socket.listen(10)

    while(True):
        client_socket, client_address = server_socket.accept()
        print(f'Connected with {client_address}')

        threading.Thread(target=serve_client, args=[client_socket]).start()

if(__name__ == '__main__'):
    main()