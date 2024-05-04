import customtkinter
import tkinter
import sqlite3

def open_loan_window():
    global loan_window, customer_id, loan_type, loan_amount, interest_rate, start_date, end_date, term

    loan_window = customtkinter.CTk(fg_color='sky blue')
    loan_window.geometry('700x650')
    loan_window.title('Loan Window')

    customer_id = customtkinter.CTkEntry(
        master=loan_window,
        width=400,
        height=40,
        placeholder_text='Customer id',
        font=('velvatica', 18)
    )

    customer_id.pack(pady=20)

    loan_type = customtkinter.CTkComboBox(
        master=loan_window,
        values=['Education', 'Home', 'Personal'],
        font=('velvatica', 18),
        dropdown_font=('velvatica', 18)
    )
    
    loan_type.pack(pady=20)

    loan_amount = customtkinter.CTkEntry(
        master=loan_window,
        width=400,
        height=40,
        placeholder_text='Loan amount',
        font=('velvatica', 18)
    )

    loan_amount.pack(pady=20)

    interest_rate = customtkinter.CTkEntry(
        master=loan_window,
        width=400,
        height=40,
        placeholder_text='Interest rate',
        font=('velvatica', 18)
    )

    interest_rate.pack(pady=20)

    start_date = customtkinter.CTkEntry(
        master=loan_window,
        width=400,
        height=40,
        placeholder_text='Start date (YYYY-MM-DD)',
        font=('velvatica', 18)
    )

    start_date.pack(pady=20)

    end_date = customtkinter.CTkEntry(
        master=loan_window,
        width=400,
        height=40,
        placeholder_text='End date (YYYY-MM-DD)',
        font=('velvatica', 18)
    )

    end_date.pack(pady=20)

    term = customtkinter.CTkEntry(
        master=loan_window,
        width=400,
        height=40,
        placeholder_text='Term (Number of months)',
        font=('velvatica', 18)
    )

    term.pack(pady=20)

    submit_button = customtkinter.CTkButton(
        master=loan_window,
        width=100,
        height=40,
        text='Submit',
        font=('velvatica', 18),
        command=store_loan_information_in_bank_database
    )

    submit_button.pack(pady=20)

    loan_window.mainloop()

def get_loan_information():
    return int(customer_id.get()), loan_type.get()[0], float(loan_amount.get()), float(interest_rate.get()), int(term.get()), start_date.get(), end_date.get(), 'A'

def store_loan_information_in_bank_database():
    connection = sqlite3.connect('bank.db')
    cursor = connection.cursor()

    loan_information = get_loan_information()

    cursor.execute('INSERT INTO loans (customer_id, loan_type, loan_amount, interest_rate, term, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', loan_information)

    connection.commit()

    cursor.close()
    connection.close()

    tkinter.messagebox.showinfo(message='Information has been saved successfully')
    loan_window.destroy()

def main():
    open_loan_window()

if(__name__ == '__main__'):
    main()