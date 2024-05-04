import customtkinter
import tkinter
import sqlite3
from datetime import datetime

def open_initial_window():
    global initial_window

    initial_window = customtkinter.CTk()
    initial_window.geometry('460x250')

    new_customer_button = customtkinter.CTkButton(
        master=initial_window,
        width=100,
        height=40,
        text='New Customer',
        font=('velvatica', 18),
        command=open_new_customer_registration_and_savings_account_creation_window
    )

    new_customer_button.pack(side=customtkinter.LEFT, padx=50)

    existing_customer_button = customtkinter.CTkButton(
        master=initial_window,
        width=100,
        height=40,
        text='Existing Customer',
        font=('velvatica', 18),
        command=open_new_savings_account_creation_window
    )

    existing_customer_button.pack(side=customtkinter.LEFT)

    initial_window.mainloop()

def open_new_customer_registration_and_savings_account_creation_window():
    global new_customer_registration_and_savings_account_creation_window, first_name, last_name, date_of_birth, address, contact_number, email, occupation, new_customer_aadhaar_number, password, new_customer_deposit_amount

    initial_window.destroy()

    new_customer_registration_and_savings_account_creation_window = customtkinter.CTk()
    new_customer_registration_and_savings_account_creation_window.geometry('700x900')
    new_customer_registration_and_savings_account_creation_window.title('New Customer Registration and Savings Account Creation Window')
    new_customer_registration_and_savings_account_creation_window.configure(fg_color='sky blue')

    first_name = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='First Name',
        font=('velvatica', 18)
    )

    first_name.pack(pady=20)

    last_name = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Last Name',
        font=('velvatica', 18)
    )

    last_name.pack(pady=20)

    date_of_birth = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Date of Birth (YYYY-MM-DD)',
        font=('velvatica', 18)
    )

    date_of_birth.pack(pady=20)

    address = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Address',
        font=('velvatica', 18)
    )

    address.pack(pady=20)

    contact_number = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Contact Number',
        font=('velvatica', 18)
    )

    contact_number.pack(pady=20)

    email = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Email',
        font=('velvatica', 18)
    )

    email.pack(pady=20)

    occupation = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Occupation',
        font=('velvatica', 18)
    )

    occupation.pack(pady=20)

    new_customer_aadhaar_number = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Aadhaar Number',
        font=('velvatica', 18)
    )

    new_customer_aadhaar_number.pack(pady=20)

    password = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Password',
        font=('velvatica', 18)
    )

    password.pack(pady=20)

    new_customer_deposit_amount = customtkinter.CTkEntry(
        master=new_customer_registration_and_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Initial Deposit Amount',
        font=('velvatica', 18)
    )

    new_customer_deposit_amount.pack(pady=20)

    submit_button = customtkinter.CTkButton(
        master=new_customer_registration_and_savings_account_creation_window,
        width=100,
        height=40,
        text='Submit',
        font=('velvatica', 18),
        command=store_new_customer_information_in_bank_database
    )

    submit_button.pack(pady=20)

    new_customer_registration_and_savings_account_creation_window.mainloop()

def get_information_of_new_customer():
    return int(new_customer_aadhaar_number.get()), password.get(), first_name.get(), last_name.get(), date_of_birth.get(), address.get(), int(contact_number.get()), email.get(), occupation.get()

def store_new_customer_information_in_bank_database():
    global connection1, cursor1

    connection1 = sqlite3.connect('bank.db')
    cursor1 = connection1.cursor()

    customer_information = get_information_of_new_customer()

    cursor1.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', customer_information)

    create_savings_account_of_new_customer()

def create_savings_account_of_new_customer():
    customer_id = new_customer_aadhaar_number.get()
    balance = new_customer_deposit_amount.get()

    date = str(datetime.now().date())

    cursor1.execute('INSERT INTO savings_accounts (customer_id, balance, open_date, status) VALUES (?, ?, ?, ?)', (customer_id, balance, date, 'Active'))

    account_number = cursor1.lastrowid

    connection1.commit()

    cursor1.close()
    connection1.close()

    tkinter.messagebox.showinfo(message=f'Your savings account has been created successfully\n\nYour account number is {account_number}')

    new_customer_registration_and_savings_account_creation_window.destroy()

def open_new_savings_account_creation_window():
    global new_savings_account_creation_window, existing_customer_aadhaar_number, existing_customer_deposit_amount
    initial_window.destroy()

    new_savings_account_creation_window = customtkinter.CTk()
    new_savings_account_creation_window.geometry('600x300')
    new_savings_account_creation_window.title('New Savings Account Creation Window')
    new_savings_account_creation_window.configure(fg_color='sky blue')

    existing_customer_aadhaar_number = customtkinter.CTkEntry(
        master=new_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Aadhaar Number',
        font=('velvatica', 18)
    )

    existing_customer_aadhaar_number.pack(pady=20)

    existing_customer_deposit_amount = customtkinter.CTkEntry(
        master=new_savings_account_creation_window,
        width=400,
        height=40,
        placeholder_text='Initial Deposit Amount',
        font=('velvatica', 18)
    )

    existing_customer_deposit_amount.pack(pady=20)

    submit_button = customtkinter.CTkButton(
        master=new_savings_account_creation_window,
        width=100,
        height=40,
        text='Submit',
        font=('velvatica', 18),
        command=create_new_savings_account_of_existing_customer
    )

    submit_button.pack(pady=20)

    new_savings_account_creation_window.mainloop()

def create_new_savings_account_of_existing_customer():
    connection2 = sqlite3.connect('bank.db')
    cursor2 = connection2.cursor()

    customer_id = existing_customer_aadhaar_number.get()
    balance = existing_customer_deposit_amount.get()

    date = str(datetime.now().date())

    cursor2.execute('INSERT INTO savings_accounts (customer_id, balance, open_date, status) VALUES (?, ?, ?, ?)', (customer_id, balance, date, 'Active'))

    account_number = cursor2.lastrowid

    connection2.commit()

    cursor2.close()
    connection2.close()

    tkinter.messagebox.showinfo(message=f'Your savings account has been created successfully\n\nYour account number is {account_number}')
    new_savings_account_creation_window.destroy()

def main():
    open_initial_window()

if(__name__ == '__main__'):
    main()
