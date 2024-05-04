import customtkinter
import tkinter
from PIL import Image, ImageTk
import socket
import threading

BANK_SERVER_ADDRESS = ('localhost', 8080)

def connect_with_bank_server():
    global client_socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(BANK_SERVER_ADDRESS)

def open_customer_verification_window():
    global customer_verification_window, customer_id, password

    customer_verification_window = customtkinter.CTk()

    customer_verification_window.geometry('500x300')
    customer_verification_window.title('Customer Verification Window')

    customer_id = customtkinter.CTkEntry(
        master=customer_verification_window,
        width=400,
        height=40,
        placeholder_text='Customer id',
        font=('velvatica', 18)
    )

    customer_id.pack(pady=25)

    password = customtkinter.CTkEntry(
        master=customer_verification_window,
        width=400,
        height=40,
        placeholder_text='Password',
        font=('velvatica', 18)
    )

    password.pack(pady=25)

    login_button = customtkinter.CTkButton(
        master=customer_verification_window,
        width=100,
        height=40,
        text='Login',
        font=('velvatica', 18),
        command=verify
    )

    login_button.pack(pady=25)

    customer_verification_window.mainloop()

def verify():
    verification_credentials = customer_id.get() + ' ' + password.get() 
    client_socket.send(verification_credentials.encode('utf-8'))

    verification_result = client_socket.recv(1024).decode('utf-8')

    if(verification_result == 'Correct'):
        tkinter.messagebox.showinfo(message='Verification successful')
        customer_verification_window.destroy()
        
        show_options()
    else:
        tkinter.messagebox.showerror(message='Incorrect credentials')
        customer_verification_window.destroy()

def show_options():
    global window

    window = customtkinter.CTk()
    window.geometry('650x200')

    check_balance_button = customtkinter.CTkButton(
        master=window,
        width=100,
        height=40,
        text='Check balance',
        font=('velvatica', 18),
        command=open_balance_check_window
    )

    check_balance_button.pack(side=customtkinter.LEFT, padx=20)

    money_transfer_button = customtkinter.CTkButton(
        master=window,
        width=100,
        height=40,
        text='Transfer money',
        font=('velvatica', 18),
        command=open_money_transfer_window
    )

    money_transfer_button.pack(side=customtkinter.LEFT, padx=20)

    window.mainloop()

def open_balance_check_window():
    global account_number, display_balance

    window.destroy()

    balance_check_window = customtkinter.CTk()
    balance_check_window.geometry('500x250')
    balance_check_window.title('Balance Check Window')

    account_number = customtkinter.CTkEntry(
        master=balance_check_window,
        width=400,
        height=40,
        placeholder_text='Account number',
        font=('velvatica', 18)
    )

    account_number.pack(pady=20)

    check_balance_button = customtkinter.CTkButton(
        master=balance_check_window,
        width=100,
        height=40,
        text='Check balance',
        font=('velvatica', 18),
        command=check_balance
    )

    check_balance_button.pack(pady=20)

    display_balance = customtkinter.CTkLabel(
        master=balance_check_window,
        width=500,
        height=40,
        fg_color='transparent',
        text='',
        font=('velvatica', 25)
    )

    display_balance.pack(pady=20)

    balance_check_window.mainloop()

def check_balance():
    client_socket.send('Check balance'.encode('utf-8'))

    client_socket.send(account_number.get().encode('utf-8'))
    balance = client_socket.recv(1024).decode('utf-8')

    display_balance.configure(text=f'Your current balance is RS {balance}')

def open_money_transfer_window():
    global money_transfer_window, sender_account_number, receiver_account_number, amount

    window.destroy()

    money_transfer_window = customtkinter.CTk()
    money_transfer_window.geometry('500x350')
    money_transfer_window.title('Money Transfer Window')

    sender_account_number = customtkinter.CTkEntry(
        master=money_transfer_window,
        width=400,
        height=40,
        placeholder_text='Your account number',
        font=('velvatica', 18)
    )

    sender_account_number.pack(pady=20)

    receiver_account_number = customtkinter.CTkEntry(
        master=money_transfer_window,
        width=400,
        height=40,
        placeholder_text='Receiver account number',
        font=('velvatica', 18)
    )

    receiver_account_number.pack(pady=20)

    amount = customtkinter.CTkEntry(
        master=money_transfer_window,
        width=400,
        height=40,
        placeholder_text='Amount',
        font=('velvatica', 18)
    )

    amount.pack(pady=20)

    transfer_money_button = customtkinter.CTkButton(
        master=money_transfer_window,
        width=100,
        height=40,
        text='Transfer',
        font=('velvatica', 18),
        command=transfer_money
    )

    transfer_money_button.pack(pady=20)

def transfer_money():
    client_socket.send('Transfer money'.encode('utf-8'))

    money_transfer_information = sender_account_number.get() + ' ' + receiver_account_number.get() + ' ' + amount.get()
    client_socket.send(money_transfer_information.encode('utf-8'))

    status = client_socket.recv(1024).decode('utf-8')

    if(status == 'Successful'):
        tkinter.messagebox.showinfo(message='Transfer is successful')
    else:
        if(status[-2] == '1'):
            tkinter.messagebox.showerror(message='Transfer has failed\n\nYou do not have sufficient balance in your account.')
        else:
            tkinter.messagebox.showerror(message='Transfer has failed\n\nThe balance in your account will be less than the minimum balance following the transfer.\nHence, the transfer is not possible.')
    
    money_transfer_window.destroy()

def main():
    connect_with_bank_server()
    open_customer_verification_window()

if(__name__ == '__main__'):
    main()

