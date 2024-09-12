from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import calendar

# Initialize the main window
root = tk.Tk()
root.geometry('400x400')
root.title('Calendar App')
root.configure(bg='#f0f0f0')  # Light gray background

# Functions to handle button actions
def show():
    m = int(month.get())
    y = int(year.get())
    output = calendar.month(y, m)
    cal.delete(1.0, 'end')  # Clear previous output
    cal.insert('end', output)

def clear():
    cal.delete(1.0, 'end')

def exit():
    root.destroy()

# Adding a header image
img = ImageTk.PhotoImage(Image.open('calendar.png'))
label = Label(root, image=img, bg='#f0f0f0')
label.place(x=170, y=10)

# Month label and input
m_label = Label(root, text="Month", font=('Verdana', 12, 'bold'), bg='#f0f0f0')
m_label.place(x=50, y=100)

month = Spinbox(root, from_=1, to=12, width=5, font=('Verdana', 10))
month.place(x=130, y=102)

# Year label and input
y_label = Label(root, text="Year", font=('Verdana', 12, 'bold'), bg='#f0f0f0')
y_label.place(x=225, y=100)

year = Spinbox(root, from_=2020, to=3000, width=8, font=('Verdana', 10))
year.place(x=290, y=102)

# Calendar display box
cal = Text(root, width=40, height=10, relief=GROOVE, borderwidth=2, font=('Consolas', 10))
cal.place(x=60, y=160)

# Buttons to control the app
show_btn = Button(root, text="Show", font=('Verdana', 10, 'bold'), relief=RAISED, borderwidth=2, command=show, bg='#4CAF50', fg='white')
show_btn.place(x=100, y=350)

clear_btn = Button(root, text="Clear", font=('Verdana', 10, 'bold'), relief=RAISED, borderwidth=2, command=clear, bg='#f0ad4e', fg='white')
clear_btn.place(x=175, y=350)

exit_btn = Button(root, text="Exit", font=('Verdana', 10, 'bold'), relief=RAISED, borderwidth=2, command=exit, bg='#d9534f', fg='white')
exit_btn.place(x=250, y=350)

# Run the main loop
root.mainloop()