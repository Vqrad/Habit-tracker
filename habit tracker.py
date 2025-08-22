import mysql.connector
from datetime import date

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
    print("Habit"+name+" added!")


def mark_done(habit_id):
    today = date.today()
    cursor.execute("INSERT INTO completions (habit_id, date) VALUES (%s, %s)", (habit_id, today))
    db.commit()
    print("Habit"+habit_id+"marked as done for"+today)


def show_progress():
    cursor.execute("""
    SELECT habits.id, habits.name, COUNT(completions.id) as days_done
    FROM habits
    LEFT JOIN completions ON habits.id = completions.habit_id
    GROUP BY habits.id, habits.name
    """)
    for (hid, name, days) in cursor.fetchall():
        print(hid,name+"- Completed "+str(days)+" days")



while True:
    print("\nHabit Tracker Menu:")
    print("1. Add Habit")
    print("2. Mark Habit as Done")
    print("3. Show Progress")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter habit name: ")
        add_habit(name)

    elif choice == "2":
        show_progress()
        hid = int(input("Enter habit ID to mark as done: "))
        mark_done(hid)

    elif choice == "3":
        show_progress()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
