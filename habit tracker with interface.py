# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 18:24:02 2025

@author: Milgard
"""

import mysql.connector
from datetime import date
import tkinter as tk
from tkinter import simpledialog, messagebox

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="varad",
    database="Habit_Tracker"
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS completions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    habit_id INT,
    date DATE,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
)
""")
db.commit()

def add_habit(name):
    cursor.execute("INSERT INTO habits (name) VALUES (%s)", (name,))
    db.commit()
    messagebox.showinfo("Success", "Habit '" + name + "' added!")

def mark_done(habit_id):
    today = date.today()
    cursor.execute("INSERT INTO completions (habit_id, date) VALUES (%s, %s)", (habit_id, today))
    db.commit()
    messagebox.showinfo("Success", "Habit " + str(habit_id) + " marked done for " + str(today))

def show_progress():
    cursor.execute("""
    SELECT habits.id, habits.name, COUNT(completions.id) as days_done
    FROM habits
    LEFT JOIN completions ON habits.id = completions.habit_id
    GROUP BY habits.id, habits.name
    """)
    rows = cursor.fetchall()
    progress_text = ""
    for (hid, name, days) in rows:
        progress_text += str(hid) + " " + name + " - Completed " + str(days) + " days\n"
    messagebox.showinfo("Progress", progress_text if progress_text else "No habits yet!")

root = tk.Tk()
root.title("Habit Tracker")
root.geometry("300x250")

tk.Label(root, text="Habit Tracker", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Add Habit", width=20, command=lambda: add_habit(simpledialog.askstring("Add Habit", "Enter habit name:"))).pack(pady=5)
tk.Button(root, text="Mark Habit as Done", width=20, command=lambda: mark_done(int(simpledialog.askstring("Mark Done", "Enter habit ID:")))).pack(pady=5)
tk.Button(root, text="Show Progress", width=20, command=show_progress).pack(pady=5)
tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=20)

root.mainloop()

