This project is a desktop-based Student Management System built in Python using Tkinter for GUI and Pickle for data storage.
It provides role-based access (Admin & Teacher) with a clean and easy-to-use interface.

🔑 Key Features
👨‍💻 Login System
<img width="429" height="298" alt="image" src="https://github.com/user-attachments/assets/fe1186f7-75d4-4161-8b24-3c4bd2c16595" />


Secure login with default users:

Admin → (username: admin, password: 1234)

Teacher → (username: teacher, password: 1234)

🏫 Admin Features

Dashboard – Quick overview of system.
<img width="1007" height="634" alt="image" src="https://github.com/user-attachments/assets/61fed7d4-5ecc-4795-a038-a5ff41e54337" />


Manage Students – Add, Edit, Delete, and View student details (Name, Roll No, Class, Age).
<img width="1366" height="733" alt="image" src="https://github.com/user-attachments/assets/26da1566-783f-4ba5-ab86-0ea5a778d452" />


Attendance – Mark and track attendance.
<img width="1357" height="710" alt="image" src="https://github.com/user-attachments/assets/4f3f6509-e155-4cd1-bb20-8770d05934a2" />

Exams/Marks – Enter and update student marks.
<img width="1260" height="642" alt="image" src="https://github.com/user-attachments/assets/63481c52-5fee-418d-ae29-40f1cac4a955" />


Fees Management – Track fee payments.
<img width="1254" height="654" alt="image" src="https://github.com/user-attachments/assets/3d843e9a-40c1-4296-8a2f-6426d349a7c7" />


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
### 👨‍💻 Author
Created by **Anuj Tiwari**
