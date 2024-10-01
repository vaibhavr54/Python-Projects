import random
import sqlite3
from twilio.rest import Client
import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
import re  # Import regex for password validation

# Twilio Configuration
account_sid = 'ACe02ead1b1bfe04f2ec543e01fc7c996d'
auth_token = '6e897da46c8ad59261657d24b938a873'
twilio_number = 'whatsapp:+14155238886'

# OTP storage
otp_dict = {}

# Database setup
def init_db():
    conn = sqlite3.connect('movie_ticket_booking_system.db')
    cursor = conn.cursor()
    
    # Create users table with phone number
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        phone TEXT NOT NULL
    )''')
    
    # Create movies table
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL
    )''')
    
    # Insert some sample movies if the table is empty
    cursor.execute("SELECT COUNT(*) FROM movies")
    if cursor.fetchone()[0] == 0:
        sample_movies = [
            ('Movie 1', 'Action', 2021),
            ('Movie 2', 'Comedy', 2020),
            ('Movie 3', 'Drama', 2022)
        ]
        cursor.executemany("INSERT INTO movies (title, genre, year) VALUES (?, ?, ?)", sample_movies)

    conn.commit()
    conn.close()

# Function to validate username
def is_valid_username(username):
    return not username[0].isdigit()  # Username must not start with a digit

# Function to validate password
def is_valid_password(password):
    # Password must be at least 8 characters long and include at least one special symbol
    return len(password) >= 8 and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

# Function to register user
def register_user(username, password, phone):
    conn = sqlite3.connect('movie_ticket_booking_system.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password, phone) VALUES (?, ?, ?)", (username, password, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Function to send an OTP via WhatsApp
def send_otp(phone):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    otp_dict[phone] = otp  # Store OTP for the session
    
    message = f'Your OTP for login is {otp}. It is valid for 5 minutes.'
    
    # Prepend '+91' to the valid phone number
    phone_with_code = f'+91{phone}'
    
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=twilio_number,
        to=f'whatsapp:{phone_with_code}',
        body=message
    )
    return otp

# Function to validate OTP
def validate_otp(phone, otp_entered):
    return otp_dict.get(phone) == otp_entered

# Function to check user credentials and send OTP
def login_user(username, password):
    conn = sqlite3.connect('movie_ticket_booking_system.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        # Send OTP to the user's phone number
        send_otp(user[3])  # phone number is at index 3
        return user
    return None

# Function to send a WhatsApp notification after booking
def send_booking_notification(phone, movie_title, customer_name, tickets):
    message = f'Tickets booked for {customer_name} for Movie: {movie_title}, Number of Tickets: {tickets}'
    
    # Prepend '+91' to the valid phone number
    phone_with_code = f'+91{phone}'
    
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=twilio_number,
        to=f'whatsapp:{phone_with_code}',
        body=message
    )

# GUI for OTP verification
def otp_verification_window(user):
    def verify_otp():
        entered_otp = int(otp_entry.get())
        phone = user[3]
        
        if validate_otp(phone, entered_otp):
            messagebox.showinfo("Success", "Login successful!")
            otp_win.destroy()
            main_app(user[3])  # Pass the user's phone number to the main app
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")
    
    otp_win = tk.Toplevel()
    otp_win.title("OTP Verification")
    
    tk.Label(otp_win, text="Enter OTP sent to your WhatsApp:").pack()
    otp_entry = tk.Entry(otp_win)
    otp_entry.pack()
    
    tk.Button(otp_win, text="Verify OTP", command=verify_otp).pack()

# Function to handle registration window
def register_window():
    def register():
        username = username_entry.get()
        password = password_entry.get()
        phone = phone_entry.get()

        # Validate username and password
        if not is_valid_username(username):
            messagebox.showerror("Error", "Username must not start with a numeric value.")
            return
        
        if not is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and include a special symbol.")
            return

        if register_user(username, password, phone):
            messagebox.showinfo("Success", "Registration successful!")
            reg_win.destroy()
        else:
            messagebox.showerror("Error", "User already exists!")

    reg_win = tk.Toplevel()
    reg_win.title("Register")

    tk.Label(reg_win, text="Username:").pack()
    username_entry = tk.Entry(reg_win)
    username_entry.pack()

    tk.Label(reg_win, text="Password:").pack()
    password_entry = tk.Entry(reg_win, show='*')
    password_entry.pack()

    tk.Label(reg_win, text="Phone Number (WhatsApp):").pack()
    phone_entry = tk.Entry(reg_win)
    phone_entry.pack()

    tk.Button(reg_win, text="Register", command=register).pack()

# Function to handle login process
def login_window():
    def login():
        username = username_entry.get()
        password = password_entry.get()

        # Validate username and password
        if not is_valid_username(username):
            messagebox.showerror("Error", "Username must not start with a numeric value.")
            return
        
        if not is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and include a special symbol.")
            return
        
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", "OTP has been sent to your WhatsApp!")
            login_win.destroy()
            otp_verification_window(user)  # Open OTP verification window
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_win = tk.Toplevel()
    login_win.title("Login")

    tk.Label(login_win, text="Username:").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password:").pack()
    password_entry = tk.Entry(login_win, show='*')
    password_entry.pack()

    tk.Button(login_win, text="Login", command=login).pack()

# GUI for main app after successful login
def main_app(user_phone):
    def book_ticket_func():
        selected_movie = selected_movie_var.get()
        customer_name = customer_name_entry.get()
        tickets = int(tickets_entry.get())
        
        # Fetch all users' phone numbers from the database
        conn = sqlite3.connect('movie_ticket_booking_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT phone FROM users")
        all_users = cursor.fetchall()
        conn.close()
        
        # Send booking notifications to all users
        for user in all_users:
            phone = user[0]
            send_booking_notification(phone, selected_movie, customer_name, tickets)
        
        messagebox.showinfo("Success", f"Tickets booked for {customer_name} for Movie: {selected_movie}! Notifications sent to all users.")
    
    main_win = tk.Toplevel()
    main_win.title("Movie Ticket Booking")

    # Fetch movie titles from the database
    conn = sqlite3.connect('movie_ticket_booking_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM movies")
    movies = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Dropdown for movie selection
    selected_movie_var = StringVar(main_win)
    selected_movie_var.set(movies[0])  # Set the default value
    tk.Label(main_win, text="Select Movie:").pack()
    movie_menu = OptionMenu(main_win, selected_movie_var, *movies)
    movie_menu.pack()

    tk.Label(main_win, text="Customer Name:").pack()
    customer_name_entry = tk.Entry(main_win)
    customer_name_entry.pack()

    tk.Label(main_win, text="Number of Tickets:").pack()
    tickets_entry = tk.Entry(main_win)
    tickets_entry.pack()

    tk.Button(main_win, text="Book Ticket", command=book_ticket_func).pack()

# Main program
if __name__ == "__main__":
    init_db()  # Initialize database
    root = tk.Tk()
    root.title("Movie Ticket Booking System")

    tk.Button(root, text="Register", command=register_window).pack(pady=10)
    tk.Button(root, text="Login", command=login_window).pack(pady=10)

    root.mainloop()