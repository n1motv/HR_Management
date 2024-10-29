import sys
import sqlite3
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore

# Connect to the SQLite database
conn = sqlite3.connect('rh_manager.db')
cursor = conn.cursor()

# Create tables if they don't exist
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        department TEXT NOT NULL,
                        position TEXT NOT NULL,
                        salary REAL NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        conge REAL DEFAULT 0,
                        last_update DATE,
                        date_of_birth DATE,
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS leave_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_id INTEGER NOT NULL,
                        type TEXT NOT NULL,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        reason TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        admin_comments TEXT,
                        FOREIGN KEY (employee_id) REFERENCES employees(id))''')
    
    conn.commit()

# Create an initial admin account
def create_admin_account():
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:  # If no users exist
        cursor.execute('''INSERT INTO users (email, password, role) VALUES (?, ?, ?)''', 
                       ('admin@example.com', 'admin123', 'admin'))
        conn.commit()

create_tables()
create_admin_account()

# Create the main application class
class EmployeeManagementApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QtWidgets.QVBoxLayout()
        
        self.title = QtWidgets.QLabel("Welcome to Employee Management System")
        self.title.setFont(QtGui.QFont("Arial", 24))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.login_button = QtWidgets.QPushButton("Login as Admin")
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px;")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def login(self):
        email, ok = QtWidgets.QInputDialog.getText(self, 'Login', 'Enter admin email:')
        if ok:
            password, ok = QtWidgets.QInputDialog.getText(self, 'Login', 'Enter password:', QtWidgets.QLineEdit.Password)
            if ok:
                if self.authenticate(email, password):
                    self.open_admin_panel()
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", "Invalid credentials")

    def authenticate(self, email, password):
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        return cursor.fetchone() is not None

    def open_admin_panel(self):
        self.admin_panel = AdminPanel()
        self.admin_panel.show()
        self.close()

class AdminPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #e0e0e0;")

        self.layout = QtWidgets.QVBoxLayout()

        self.title = QtWidgets.QLabel("Admin Panel")
        self.title.setFont(QtGui.QFont("Arial", 24))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.add_employee_button = QtWidgets.QPushButton("Add Employee")
        self.add_employee_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 18px; padding: 10px;")
        self.add_employee_button.clicked.connect(self.add_employee)
        self.layout.addWidget(self.add_employee_button)

        self.view_employees_button = QtWidgets.QPushButton("View Employees")
        self.view_employees_button.setStyleSheet("background-color: #FF9800; color: white; font-size: 18px; padding: 10px;")
        self.view_employees_button.clicked.connect(self.view_employees)
        self.layout.addWidget(self.view_employees_button)

        self.update_employee_button = QtWidgets.QPushButton("Update Employee")
        self.update_employee_button.setStyleSheet("background-color: #FF5722; color: white; font-size: 18px; padding: 10px;")
        self.update_employee_button.clicked.connect(self.update_employee)
        self.layout.addWidget(self.update_employee_button)

        self.delete_employee_button = QtWidgets.QPushButton("Delete Employee")
        self.delete_employee_button.setStyleSheet("background-color: #F44336; color: white; font-size: 18px; padding: 10px;")
        self.delete_employee_button.clicked.connect(self.delete_employee)
        self.layout.addWidget(self.delete_employee_button)

        self.view_leave_requests_button = QtWidgets.QPushButton("View Leave Requests")
        self.view_leave_requests_button.setStyleSheet("background-color: #9C27B0; color: white; font-size: 18px; padding: 10px;")
        self.view_leave_requests_button.clicked.connect(self.view_leave_requests)
        self.layout.addWidget(self.view_leave_requests_button)

        self.setLayout(self.layout)

    def add_employee(self):
        first_name, ok1 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'First Name:')
        if not ok1: return
        last_name, ok2 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'Last Name:')
        if not ok2: return
        department, ok3 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'Department:')
        if not ok3: return
        position, ok4 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'Position:')
        if not ok4: return
        salary, ok5 = QtWidgets.QInputDialog.getDouble(self, 'Add Employee', 'Salary:', min=0)
        if not ok5: return
        email, ok6 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'Email:')
        if not ok6: return
        emp_password, ok7 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'Password:', QtWidgets.QLineEdit.Password)
        if not ok7: return
        date_of_birth, ok8 = QtWidgets.QInputDialog.getText(self, 'Add Employee', 'Date of Birth (YYYY-MM-DD):')
        if not ok8: return

        try:
            cursor.execute('''INSERT INTO employees (first_name, last_name, department, position, salary, email, conge, date_of_birth)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (first_name, last_name, department, position, salary, email, 0, date_of_birth))
            cursor.execute('''INSERT INTO users (email, password, role)
                              VALUES (?, ?, ?)''', (email, emp_password, 'employee'))
            conn.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Employee added successfully!")
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Error", "Email already in use.")

    def view_employees(self):
        employees = cursor.execute('SELECT * FROM employees').fetchall()
        employee_list = '\n'.join([f"{emp[0]}: {emp[1]} {emp[2]}, {emp[3]}, {emp[4]}, {emp[5]}, {emp[6]}" for emp in employees])
        QtWidgets.QMessageBox.information(self, "Employees", employee_list or "No employees found.")

    def update_employee(self):
        emp_id, ok = QtWidgets.QInputDialog.getInt(self, 'Update Employee', 'Enter Employee ID:')
        if not ok: return
        new_salary, ok = QtWidgets.QInputDialog.getDouble(self, 'Update Employee', 'New Salary:', min=0)
        if not ok: return

        cursor.execute('UPDATE employees SET salary = ? WHERE id = ?', (new_salary, emp_id))
        conn.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Employee updated successfully!")

    def delete_employee(self):
        emp_id, ok = QtWidgets.QInputDialog.getInt(self, 'Delete Employee', 'Enter Employee ID to delete:')
        if not ok: return

        cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
        conn.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Employee deleted successfully!")

    def view_leave_requests(self):
        leave_requests = cursor.execute('SELECT * FROM leave_requests').fetchall()
        requests_list = '\n'.join([f"ID: {req[0]}, Emp ID: {req[1]}, Type: {req[2]}, Start: {req[3]}, End: {req[4]}, Status: {req[6]}" for req in leave_requests])
        QtWidgets.QMessageBox.information(self, "Leave Requests", requests_list or "No leave requests found.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = EmployeeManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
