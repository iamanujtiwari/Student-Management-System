This project is a desktop-based Student Management System built in Python using Tkinter for GUI and Pickle for data storage.
It provides role-based access (Admin & Teacher) with a clean and easy-to-use interface.

🔑 Key Features
👨‍💻 Login System

Secure login with default users:

Admin → (username: admin, password: 1234)

Teacher → (username: teacher, password: 1234)

🏫 Admin Features

Dashboard – Quick overview of system.

Manage Students – Add, Edit, Delete, and View student details (Name, Roll No, Class, Age).

Attendance – Mark and track attendance.

Exams/Marks – Enter and update student marks.

Fees Management – Track fee payments.

Logout – Securely exit to login screen.

👩‍🏫 Teacher Features

Dashboard – Teacher’s workspace.

View Students – Access list of students (read-only).

Mark Attendance – Update daily attendance.

Enter Marks – Record exam/test scores.

Logout – Return to login.

📂 Data Storage

Data is stored persistently using Pickle (.pkl) files inside a data/ folder:

users.pkl → Stores login credentials

students.pkl → Stores student records

attendance.pkl → Stores attendance data

exams.pkl → Stores exam marks

fees.pkl → Stores fee details

🖥️ Technology Stack

Python 3.x

Tkinter (GUI library)

Pickle (for file-based database storage)

🚀 How to Run

Save the Python file 

Run in terminal/IDE:

python gui.py


Login as Admin or Teacher.

Start managing student records, attendance, marks, and fees.
