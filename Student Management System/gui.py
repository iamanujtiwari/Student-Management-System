import os
import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# ------------------------------
# Persistent storage via pickle
# ------------------------------
DATA_DIR = 'data'
FILES = {
    'users': os.path.join(DATA_DIR, 'users.pkl'),
    'students': os.path.join(DATA_DIR, 'students.pkl'),
    'attendance': os.path.join(DATA_DIR, 'attendance.pkl'),
    'exams': os.path.join(DATA_DIR, 'exams.pkl'),
    'fees': os.path.join(DATA_DIR, 'fees.pkl'),
}

os.makedirs(DATA_DIR, exist_ok=True)

def load_pickle(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return default

def save_pickle(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

# Seed default users if not present
users = load_pickle(FILES['users'], {})
if not users:
    users = {
        'admin': {'password': '1234', 'role': 'admin'},
        'teacher': {'password': '1234', 'role': 'teacher'},
    }
    save_pickle(FILES['users'], users)

students = load_pickle(FILES['students'], [])  # list of dicts: {id, roll, name, clazz, contact}
attendance = load_pickle(FILES['attendance'], {})  # key: (student_id, 'YYYY-MM-DD') -> 'P'/'A'
exams = load_pickle(FILES['exams'], [])  # list of dicts: {id, student_id, subject, marks, max_marks, date}
fees = load_pickle(FILES['fees'], {})  # student_id -> {total, paid, history:[{date, amount}]}

# Helpers to persist whenever data changes
def persist_all():
    save_pickle(FILES['users'], users)
    save_pickle(FILES['students'], students)
    save_pickle(FILES['attendance'], attendance)
    save_pickle(FILES['exams'], exams)
    save_pickle(FILES['fees'], fees)

# ------------------------------
# UI Helpers / Theme
# ------------------------------
APP_BG = '#f5f6fa'
HEADER_BG = '#273c75'
SIDE_BG = '#dcdde1'
BTN_BG = '#718093'

class App:
    def __init__(self):
        self.login_win = None
        self.root = None
        self.role = None
        self.username = None
        self._student_auto_id = self.compute_next_student_id()
        self._exam_auto_id = self.compute_next_exam_id()
        self.open_login()

    def compute_next_student_id(self):
        return (max([s['id'] for s in students], default=0) + 1)

    def compute_next_exam_id(self):
        return (max([e['id'] for e in exams], default=0) + 1)

    # ---------------- Login ----------------
    def open_login(self):
        if self.root:
            try:
                self.root.destroy()
            except Exception:
                pass
        self.login_win = tk.Tk()
        self.login_win.title('Login - Student Management System')
        self.login_win.geometry('420x260')
        self.login_win.config(bg=SIDE_BG)

        tk.Label(self.login_win, text='🔐 Login', font=('Arial', 18, 'bold'), bg=SIDE_BG).pack(pady=18)
        frm = tk.Frame(self.login_win, bg=SIDE_BG)
        frm.pack(pady=6)
        tk.Label(frm, text='Username:', font=('Arial', 12), bg=SIDE_BG).grid(row=0, column=0, sticky='e', padx=6, pady=6)
        tk.Label(frm, text='Password:', font=('Arial', 12), bg=SIDE_BG).grid(row=1, column=0, sticky='e', padx=6, pady=6)
        self.ent_user = tk.Entry(frm, font=('Arial', 12))
        self.ent_pass = tk.Entry(frm, font=('Arial', 12), show='*')
        self.ent_user.grid(row=0, column=1, padx=6, pady=6)
        self.ent_pass.grid(row=1, column=1, padx=6, pady=6)
        tk.Button(self.login_win, text='Login', font=('Arial', 12, 'bold'), bg=HEADER_BG, fg='white',
                  command=self.handle_login).pack(pady=14)
        self.ent_user.focus_set()
        self.login_win.mainloop()

    def handle_login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        if u in users and users[u]['password'] == p:
            self.role = users[u]['role']
            self.username = u
            self.login_win.destroy()
            self.open_dashboard()
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password')

    # --------------- Dashboard ---------------
    def open_dashboard(self):
        self.root = tk.Tk()
        self.root.title('📚 Student Management Software')
        self.root.geometry('1000x640')
        self.root.config(bg=APP_BG)

        header = tk.Label(self.root, text=f'📚 Student Management Software  ({self.role.capitalize()} Mode)',
                          bg=HEADER_BG, fg='white', font=('Arial', 18, 'bold'), pady=10)
        header.pack(fill='x')

        sidebar = tk.Frame(self.root, bg=SIDE_BG, width=220)
        sidebar.pack(side='left', fill='y')

        self.content = tk.Frame(self.root, bg='white')
        self.content.pack(side='right', fill='both', expand=True)

        # Buttons by role
        if self.role == 'admin':
            items = [
                ('Dashboard', self.show_dashboard),
                ('Students', self.show_students),
                ('Attendance', self.show_attendance),
                ('Exams', self.show_exams),
                ('Fees', self.show_fees),
                ('Logout', self.logout)
            ]
        else:  # teacher
            items = [
                ('Dashboard', self.show_dashboard),
                ('Mark Attendance', self.show_attendance),
                ('Enter Marks', self.show_exams),
                ('View Students', self.show_students_readonly),
                ('Logout', self.logout)
            ]

        for text, cmd in items:
            tk.Button(sidebar, text=text, font=('Arial', 12), bg=BTN_BG, fg='white', relief='flat',
                      padx=10, pady=12, command=cmd).pack(fill='x', pady=3)

        self.show_dashboard()
        self.root.mainloop()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # --------------- Views ---------------
    def show_dashboard(self):
        self.clear_content()
        tk.Label(self.content, text=f"Welcome, {self.username} 👋", font=('Arial', 18, 'bold'), bg='white').pack(pady=16)

        # Simple stats
        total_students = len(students)
        total_exams = len(exams)
        total_present_today = sum(1 for s in students if attendance.get((s['id'], date.today().isoformat())) == 'P')

        grid = tk.Frame(self.content, bg='white')
        grid.pack(pady=10)
        def stat_card(parent, title, value):
            card = tk.Frame(parent, bg=APP_BG, bd=0, relief='flat')
            card.pack(side='left', padx=12)
            tk.Label(card, text=title, font=('Arial', 12)).pack(padx=30, pady=(12, 2))
            tk.Label(card, text=str(value), font=('Arial', 20, 'bold')).pack(padx=30, pady=(0, 12))
        stat_card(grid, 'Total Students', total_students)
        stat_card(grid, 'Exam Records', total_exams)
        stat_card(grid, 'Present Today', total_present_today)

    # ---------- Students (Admin full / Teacher readonly) ----------
    def _students_table(self, parent, with_actions=True):
        cols = ('id', 'roll', 'name', 'clazz', 'contact')
        tree = ttk.Treeview(parent, columns=cols, show='headings', height=15)
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=130 if c != 'name' else 220)
        tree.pack(fill='both', expand=True, pady=10)
        self.refresh_students_table(tree)

        if with_actions:
            btns = tk.Frame(parent, bg='white')
            btns.pack(pady=6)
            tk.Button(btns, text='Add', command=self.add_student_popup).pack(side='left', padx=6)
            tk.Button(btns, text='Edit', command=lambda: self.edit_student_popup(tree)).pack(side='left', padx=6)
            tk.Button(btns, text='Delete', command=lambda: self.delete_student(tree)).pack(side='left', padx=6)
            tk.Button(btns, text='Search', command=lambda: self.search_student_popup(tree)).pack(side='left', padx=6)
        return tree

    def refresh_students_table(self, tree):
        for i in tree.get_children():
            tree.delete(i)
        for s in students:
            tree.insert('', 'end', values=(s['id'], s['roll'], s['name'], s['clazz'], s['contact']))

    def show_students(self):
        self.clear_content()
        tk.Label(self.content, text='Manage Students', font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        self._students_table(self.content, with_actions=True)

    def show_students_readonly(self):
        self.clear_content()
        tk.Label(self.content, text='Students', font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        self._students_table(self.content, with_actions=False)

    def add_student_popup(self):
        win = tk.Toplevel(self.root)
        win.title('Add Student')
        self._student_form(win)

    def edit_student_popup(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Select', 'Please select a student to edit')
            return
        item = tree.item(sel[0])['values']
        sid = item[0]
        data = next((s for s in students if s['id'] == sid), None)
        if not data:
            return
        win = tk.Toplevel(self.root)
        win.title('Edit Student')
        self._student_form(win, data)

    def _student_form(self, win, data=None):
        frm = tk.Frame(win, padx=10, pady=10)
        frm.pack()
        tk.Label(frm, text='Roll No').grid(row=0, column=0, sticky='e', padx=6, pady=6)
        tk.Label(frm, text='Name').grid(row=1, column=0, sticky='e', padx=6, pady=6)
        tk.Label(frm, text='Class').grid(row=2, column=0, sticky='e', padx=6, pady=6)
        tk.Label(frm, text='Contact').grid(row=3, column=0, sticky='e', padx=6, pady=6)

        ent_roll = tk.Entry(frm); ent_name = tk.Entry(frm); ent_class = tk.Entry(frm); ent_contact = tk.Entry(frm)
        ent_roll.grid(row=0, column=1); ent_name.grid(row=1, column=1); ent_class.grid(row=2, column=1); ent_contact.grid(row=3, column=1)
        if data:
            ent_roll.insert(0, data['roll']); ent_name.insert(0, data['name']); ent_class.insert(0, data['clazz']); ent_contact.insert(0, data['contact'])

        def save_student():
            roll = ent_roll.get().strip(); name = ent_name.get().strip(); clazz = ent_class.get().strip(); contact = ent_contact.get().strip()
            if not roll or not name:
                messagebox.showerror('Validation', 'Roll No and Name are required')
                return
            # unique roll
            if data:
                # editing
                for s in students:
                    if s['roll'] == roll and s['id'] != data['id']:
                        messagebox.showerror('Duplicate', 'Roll No already exists')
                        return
                data.update({'roll': roll, 'name': name, 'clazz': clazz, 'contact': contact})
            else:
                if any(s['roll'] == roll for s in students):
                    messagebox.showerror('Duplicate', 'Roll No already exists')
                    return
                new_stu = {'id': self._student_auto_id, 'roll': roll, 'name': name, 'clazz': clazz, 'contact': contact}
                students.append(new_stu)
                if new_stu['id'] not in fees:
                    fees[new_stu['id']] = {'total': 0.0, 'paid': 0.0, 'history': []}
                self._student_auto_id += 1
            persist_all()
            messagebox.showinfo('Saved', 'Student saved successfully')
            win.destroy()
            self.show_students()

        tk.Button(frm, text='Save', command=save_student).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_student(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Select', 'Please select a student to delete')
            return
        item = tree.item(sel[0])['values']
        sid = item[0]
        if messagebox.askyesno('Confirm', 'Delete selected student?'):
            global students
            students[:] = [s for s in students if s['id'] != sid]
            # cascade delete attendance/exams/fees entries
            keys = [k for k in list(attendance.keys()) if k[0] == sid]
            for k in keys:
                del attendance[k]
            global exams
            exams[:] = [e for e in exams if e['student_id'] != sid]
            if sid in fees:
                del fees[sid]
            persist_all()
            self.show_students()

    def search_student_popup(self, tree):
        win = tk.Toplevel(self.root)
        win.title('Search Student')
        tk.Label(win, text='Name or Roll contains:').pack(side='left', padx=6, pady=10)
        ent = tk.Entry(win)
        ent.pack(side='left', padx=6)
        def do_search():
            query = ent.get().lower().strip()
            for i in tree.get_children():
                tree.delete(i)
            for s in students:
                if query in s['name'].lower() or query in s['roll'].lower():
                    tree.insert('', 'end', values=(s['id'], s['roll'], s['name'], s['clazz'], s['contact']))
        tk.Button(win, text='Search', command=do_search).pack(side='left', padx=6)

    # ---------- Attendance ----------
    def show_attendance(self):
        self.clear_content()
        tk.Label(self.content, text='Attendance', font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        top = tk.Frame(self.content, bg='white'); top.pack(pady=4)
        tk.Label(top, text='Date (YYYY-MM-DD):', bg='white').pack(side='left', padx=6)
        self.att_date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(top, textvariable=self.att_date_var, width=12).pack(side='left', padx=6)
        tk.Button(top, text='Load', command=self.refresh_attendance_list).pack(side='left', padx=6)
        tk.Button(top, text='Save All', command=self.save_attendance_all).pack(side='left', padx=6)

        self.att_list = tk.Frame(self.content, bg='white')
        self.att_list.pack(fill='both', expand=True, pady=8)
        self.att_vars = {}  # sid -> tk.StringVar('P'/'A')
        self.refresh_attendance_list()

    def refresh_attendance_list(self):
        for w in self.att_list.winfo_children():
            w.destroy()
        self.att_vars = {}
        d = self.att_date_var.get().strip()
        if not d:
            d = date.today().isoformat()
            self.att_date_var.set(d)
        header = tk.Frame(self.att_list, bg='white'); header.pack(fill='x')
        tk.Label(header, text='Roll', width=10, anchor='w', bg='white', font=('Arial', 10, 'bold')).pack(side='left')
        tk.Label(header, text='Name', width=28, anchor='w', bg='white', font=('Arial', 10, 'bold')).pack(side='left')
        tk.Label(header, text='Status', width=12, anchor='w', bg='white', font=('Arial', 10, 'bold')).pack(side='left')
        for s in students:
            row = tk.Frame(self.att_list, bg='white'); row.pack(fill='x', pady=1)
            tk.Label(row, text=s['roll'], width=10, anchor='w', bg='white').pack(side='left')
            tk.Label(row, text=s['name'], width=28, anchor='w', bg='white').pack(side='left')
            var = tk.StringVar(value=attendance.get((s['id'], d), 'A'))
            self.att_vars[s['id']] = var
            cb = ttk.Combobox(row, values=['P', 'A'], textvariable=var, width=5, state='readonly')
            cb.pack(side='left', padx=6)

    def save_attendance_all(self):
        d = self.att_date_var.get().strip()
        for sid, var in self.att_vars.items():
            attendance[(sid, d)] = var.get()
        persist_all()
        messagebox.showinfo('Saved', 'Attendance saved')

    # ---------- Exams / Marks ----------
    def show_exams(self):
        self.clear_content()
        tk.Label(self.content, text='Exams / Marks', font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        top = tk.Frame(self.content, bg='white'); top.pack(pady=6)
        tk.Label(top, text='Student:').grid(row=0, column=0, padx=4, pady=4)
        stu_names = [f"{s['id']} - {s['name']}" for s in students]
        self.exam_stu_var = tk.StringVar()
        ttk.Combobox(top, textvariable=self.exam_stu_var, values=stu_names, width=28, state='readonly').grid(row=0, column=1, padx=4, pady=4)
        tk.Label(top, text='Subject:').grid(row=0, column=2, padx=4, pady=4)
        self.exam_sub_var = tk.StringVar(); tk.Entry(top, textvariable=self.exam_sub_var, width=16).grid(row=0, column=3, padx=4, pady=4)
        tk.Label(top, text='Marks:').grid(row=0, column=4, padx=4, pady=4)
        self.exam_marks_var = tk.StringVar(); tk.Entry(top, textvariable=self.exam_marks_var, width=8).grid(row=0, column=5, padx=4, pady=4)
        tk.Label(top, text='Max:').grid(row=0, column=6, padx=4, pady=4)
        self.exam_max_var = tk.StringVar(); tk.Entry(top, textvariable=self.exam_max_var, width=8).grid(row=0, column=7, padx=4, pady=4)
        tk.Label(top, text='Date:').grid(row=0, column=8, padx=4, pady=4)
        self.exam_date_var = tk.StringVar(value=date.today().isoformat()); tk.Entry(top, textvariable=self.exam_date_var, width=12).grid(row=0, column=9, padx=4, pady=4)
        tk.Button(top, text='Add/Update', command=self.add_exam_record).grid(row=0, column=10, padx=6)

        # table
        self.exam_table = ttk.Treeview(self.content, columns=('id', 'student_id', 'name', 'subject', 'marks', 'max', 'date'), show='headings', height=14)
        for c, w in zip(('id', 'student_id', 'name', 'subject', 'marks', 'max', 'date'), (60, 80, 160, 120, 80, 80, 100)):
            self.exam_table.heading(c, text=c.capitalize())
            self.exam_table.column(c, width=w)
        self.exam_table.pack(fill='both', expand=True, pady=8)
        self.refresh_exam_table()

    def add_exam_record(self):
        stu_label = self.exam_stu_var.get()
        if not stu_label:
            messagebox.showerror('Select', 'Select a student')
            return
        sid = int(stu_label.split(' - ')[0])
        subject = self.exam_sub_var.get().strip()
        try:
            marks = float(self.exam_marks_var.get())
            maxm = float(self.exam_max_var.get())
        except ValueError:
            messagebox.showerror('Validation', 'Marks and Max must be numbers')
            return
        dt = self.exam_date_var.get().strip() or date.today().isoformat()
        rec = {'id': self._exam_auto_id, 'student_id': sid, 'subject': subject, 'marks': marks, 'max_marks': maxm, 'date': dt}
        exams.append(rec)
        self._exam_auto_id += 1
        persist_all()
        self.refresh_exam_table()
        messagebox.showinfo('Saved', 'Exam record saved')

    def refresh_exam_table(self):
        for i in self.exam_table.get_children():
            self.exam_table.delete(i)
        # Show joined with name
        id_to_name = {s['id']: s['name'] for s in students}
        for e in exams:
            self.exam_table.insert('', 'end', values=(e['id'], e['student_id'], id_to_name.get(e['student_id'], '?'), e['subject'], e['marks'], e['max_marks'], e['date']))

    # ---------- Fees ----------
    def show_fees(self):
        self.clear_content()
        tk.Label(self.content, text='Fees', font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        top = tk.Frame(self.content, bg='white'); top.pack(pady=6)
        tk.Label(top, text='Student:').grid(row=0, column=0, padx=4, pady=4)
        stu_names = [f"{s['id']} - {s['name']}" for s in students]
        self.fee_stu_var = tk.StringVar()
        ttk.Combobox(top, textvariable=self.fee_stu_var, values=stu_names, width=28, state='readonly').grid(row=0, column=1, padx=4, pady=4)
        tk.Label(top, text='Total Fee:').grid(row=0, column=2, padx=4, pady=4)
        self.total_fee_var = tk.StringVar(); tk.Entry(top, textvariable=self.total_fee_var, width=10).grid(row=0, column=3, padx=4, pady=4)
        tk.Button(top, text='Set Total', command=self.set_total_fee).grid(row=0, column=4, padx=6)
        tk.Label(top, text='Pay Amount:').grid(row=0, column=5, padx=4, pady=4)
        self.pay_amt_var = tk.StringVar(); tk.Entry(top, textvariable=self.pay_amt_var, width=10).grid(row=0, column=6, padx=4, pady=4)
        tk.Button(top, text='Add Payment', command=self.add_payment).grid(row=0, column=7, padx=6)

        self.fee_info = tk.Label(self.content, text='Select a student to view fee details', bg='white', font=('Arial', 12))
        self.fee_info.pack(pady=6)

        self.fee_table = ttk.Treeview(self.content, columns=('date', 'amount'), show='headings', height=12)
        self.fee_table.heading('date', text='Date')
        self.fee_table.heading('amount', text='Amount')
        self.fee_table.column('date', width=120)
        self.fee_table.column('amount', width=120)
        self.fee_table.pack(pady=6)

        # Update fee panel when student selection changes
        def on_stu_change(*_):
            self.refresh_fee_view()
        self.fee_stu_var.trace_add('write', on_stu_change)

    def set_total_fee(self):
        label = self.fee_stu_var.get()
        if not label:
            messagebox.showerror('Select', 'Select a student')
            return
        sid = int(label.split(' - ')[0])
        try:
            total = float(self.total_fee_var.get())
        except ValueError:
            messagebox.showerror('Validation', 'Total must be a number')
            return
        acc = fees.setdefault(sid, {'total': 0.0, 'paid': 0.0, 'history': []})
        acc['total'] = total
        persist_all()
        self.refresh_fee_view()
        messagebox.showinfo('Saved', 'Total fee set')

    def add_payment(self):
        label = self.fee_stu_var.get()
        if not label:
            messagebox.showerror('Select', 'Select a student')
            return
        sid = int(label.split(' - ')[0])
        try:
            amt = float(self.pay_amt_var.get())
        except ValueError:
            messagebox.showerror('Validation', 'Amount must be a number')
            return
        acc = fees.setdefault(sid, {'total': 0.0, 'paid': 0.0, 'history': []})
        acc['paid'] += amt
        acc['history'].append({'date': date.today().isoformat(), 'amount': amt})
        persist_all()
        self.refresh_fee_view()
        messagebox.showinfo('Saved', 'Payment added')

    def refresh_fee_view(self):
        # clear table
        for i in self.fee_table.get_children():
            self.fee_table.delete(i)
        label = self.fee_stu_var.get()
        if not label:
            self.fee_info.config(text='Select a student to view fee details')
            return
        sid = int(label.split(' - ')[0])
        acc = fees.setdefault(sid, {'total': 0.0, 'paid': 0.0, 'history': []})
        bal = acc['total'] - acc['paid']
        self.fee_info.config(text=f"Total: {acc['total']}   Paid: {acc['paid']}   Balance: {bal}")
        for h in acc['history']:
            self.fee_table.insert('', 'end', values=(h['date'], h['amount']))

    # ---------- Logout ----------
    def logout(self):
        if messagebox.askyesno('Logout', 'Do you really want to logout?'):
            try:
                self.root.destroy()
            except Exception:
                pass
            self.role = None
            self.username = None
            self.open_login()

if __name__ == '__main__':
    App()
