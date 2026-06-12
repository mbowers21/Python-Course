# Database.py interfaces between sqlite3 and Main.py
import sqlite3
DB_PATH = "company_w5.db"
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                location TEXT
            )
        """)
def get_all_employees():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT e.id, e.name, d.name AS department, e.salary
                       FROM employees e
                       LEFT JOIN departments d ON e.department_id = d.id
                       ORDER BY e.name
        """)
        return cursor.fetchall()
def add_employee(name, salary, department_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO employees (name, salary, department_id)
                       VALUES (?, ?, ?)""", 
                       (name, salary, department_id))
        connection.commit()
        return cursor.lastrowid
def update_salary(employee_id, new_salary):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""UPDATE employees
                       SET salary = ?
                       WHERE id = ?""", 
                       (new_salary, employee_id))
        connection.commit()
        return cursor.rowcount
def delete_employee(employee_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM employees
                       WHERE id = ?""", (employee_id,))
        connection.commit()
        return cursor.rowcount
def get_employee_by_id(employee_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT e.id, e.name, d.name AS department, e.salary
                       FROM employees e
                       LEFT JOIN departments d ON e.department_id = d.id
                       WHERE e.id = ?""", (employee_id,))
        return cursor.fetchone()
def get_all_departments():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT d.id, d.name, d.location, COUNT(e.id) AS employee_count
                       FROM departments d
                       LEFT JOIN employees e ON d.id = e.department_id
                       GROUP BY d.id, d.name, d.location
                       ORDER BY d.name
        """)
        return cursor.fetchall()
def get_department_by_id(department_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT d.id, d.name, d.location, COUNT(e.id) AS employee_count
                       FROM departments d
                       LEFT JOIN employees e ON d.id = e.department_id
                       WHERE d.id = ?
                       GROUP BY d.id, d.name, d.location
        """, (department_id,))
        return cursor.fetchone()
def add_department(name, location = ""):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO departments (name, location)
                       VALUES (?, ?)""", 
                       (name, location))
        connection.commit()
        return cursor.lastrowid
def update_department_location(department_id, location):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""UPDATE departments
                       SET location = ?
                       WHERE id = ?""", 
                       (location, department_id))
        connection.commit()
        return cursor.rowcount
def update_department_name(department_id, name):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""UPDATE departments
                       SET name = ?
                       WHERE id = ?""", 
                       (name, department_id))
        connection.commit()
        return cursor.rowcount
def get_employees_by_department(department_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT e.id, e.name, e.salary
                       FROM employees e
                       WHERE e.department_id = ?
                       ORDER BY e.name""", (department_id,))
        return cursor.fetchall()