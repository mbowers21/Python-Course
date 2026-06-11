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