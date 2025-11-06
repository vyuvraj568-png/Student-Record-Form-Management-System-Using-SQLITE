from tkinter import *
from tkinter import messagebox, ttk
import sqlite3

root = Tk()
root.title("Student Record Management System (SQLite Enhanced)")
root.geometry("600x600")
root.config(bg="#f0f4f7")

# ---------------------------
# Database Setup
# ---------------------------
db_name = "student_records.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    roll TEXT PRIMARY KEY,
    marks REAL
)
""")
conn.commit()

# ---------------------------
# Functions
# ---------------------------
def add_record():
    name = name_entry.get()
    roll = roll_entry.get()
    marks = marks_entry.get()

    if name == "" or roll == "" or marks == "":
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    try:
        cursor.execute("INSERT INTO students (name, roll, marks) VALUES (?, ?, ?)", (name, roll, marks))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
        clear_fields()
        show_records()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"Roll No {roll} already exists!")

def show_records(order_by=None):
    text_box.delete("1.0", END)
    query = "SELECT * FROM students"
    if order_by == "name":
        query += " ORDER BY name ASC"
    elif order_by == "marks":
        query += " ORDER BY marks DESC"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        text_box.insert(END, "No records found.\n")
    else:
        text_box.insert(END, f"{'Name':<20} {'Roll No':<10} {'Marks':<10}\n")
        text_box.insert(END, "-"*45 + "\n")
        for row in rows:
            text_box.insert(END, f"{row[0]:<20} {row[1]:<10} {row[2]:<10}\n")

def search_record():
    roll = roll_entry.get()
    if roll == "":
        messagebox.showwarning("Input Error", "Please enter Roll No to search!")
        return
    cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
    row = cursor.fetchone()
    text_box.delete("1.0", END)
    if row:
        text_box.insert(END, f"Found ->\nName: {row[0]}\nRoll No: {row[1]}\nMarks: {row[2]}")
    else:
        messagebox.showinfo("Not Found", f"No record found with Roll No: {roll}")

def delete_record():
    roll = roll_entry.get()
    if roll == "":
        messagebox.showwarning("Input Error", "Please enter Roll No to delete!")
        return

    cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
        conn.commit()
        messagebox.showinfo("Deleted", f"Record with Roll No {roll} deleted successfully!")
        show_records()
    else:
        messagebox.showinfo("Not Found", f"No record found with Roll No: {roll}")

def update_record():
    roll = roll_entry.get()
    new_name = name_entry.get()
    new_marks = marks_entry.get()

    if roll == "":
        messagebox.showwarning("Input Error", "Please enter Roll No to update!")
        return

    cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
    row = cursor.fetchone()
    if not row:
        messagebox.showinfo("Not Found", f"No record found with Roll No: {roll}")
        return

    if new_name == "":
        new_name = row[0]
    if new_marks == "":
        new_marks = row[2]

    cursor.execute("UPDATE students SET name=?, marks=? WHERE roll=?", (new_name, new_marks, roll))
    conn.commit()
    messagebox.showinfo("Updated", f"Record with Roll No {roll} updated successfully!")
    show_records()

def total_students():
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    messagebox.showinfo("Total Students", f"Total number of students: {count}")

def clear_fields():
    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    marks_entry.delete(0, END)

# ---------------------------
# GUI Layout
# ---------------------------
Label(root, text="STUDENT RECORD MANAGEMENT SYSTEM", font=("Arial", 16, "bold"), bg="#4a90e2", fg="white", padx=10, pady=10).pack(fill=X)

frame = Frame(root, bg="#f0f4f7")
frame.pack(pady=10)

Label(frame, text="Name:", bg="#f0f4f7", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
name_entry = Entry(frame, width=30)
name_entry.grid(row=0, column=1)

Label(frame, text="Roll No:", bg="#f0f4f7", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
roll_entry = Entry(frame, width=30)
roll_entry.grid(row=1, column=1)

Label(frame, text="Marks:", bg="#f0f4f7", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
marks_entry = Entry(frame, width=30)
marks_entry.grid(row=2, column=1)

btn_frame = Frame(root, bg="#f0f4f7")
btn_frame.pack(pady=10)

Button(btn_frame, text="Add Record", bg="#81c784", command=add_record, width=15).grid(row=0, column=0, padx=5, pady=5)
Button(btn_frame, text="Show All", bg="#64b5f6", command=show_records, width=15).grid(row=0, column=1, padx=5, pady=5)
Button(btn_frame, text="Search", bg="#ffd54f", command=search_record, width=15).grid(row=0, column=2, padx=5, pady=5)
Button(btn_frame, text="Delete", bg="#e57373", command=delete_record, width=15).grid(row=1, column=0, padx=5, pady=5)
Button(btn_frame, text="Update", bg="#ba68c8", command=update_record, width=15).grid(row=1, column=1, padx=5, pady=5)
Button(btn_frame, text="Total Students", bg="#4db6ac", command=total_students, width=15).grid(row=1, column=2, padx=5, pady=5)

sort_frame = Frame(root, bg="#f0f4f7")
sort_frame.pack(pady=5)
Label(sort_frame, text="Sort By:", bg="#f0f4f7").pack(side=LEFT)
Button(sort_frame, text="Name", bg="#aed581", command=lambda: show_records("name")).pack(side=LEFT, padx=5)
Button(sort_frame, text="Marks", bg="#90caf9", command=lambda: show_records("marks")).pack(side=LEFT, padx=5)

# Output display
text_box = Text(root, width=70, height=15, bg="#ffffff", fg="#333333", font=("Courier New", 10))
text_box.pack(pady=10)

show_records()

root.mainloop()
conn.close()
