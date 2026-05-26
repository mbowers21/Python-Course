import sqlite3
connection = sqlite3.connect('company.db')
cursor = connection.cursor()
#Creating Tables
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    name     TEXT NOT NULL,
                    age      INTEGER,
                    city     TEXT,
                    salary   REAL NOT NULL
                   )''')
connection.commit()
connection.close()
#Inserting Data
connection = sqlite3.connect('company.db')
cursor = connection.cursor()
#Inputting one row of information
cursor.execute('''INSERT INTO employees (
                   name, age, city, salary)
                   VALUES (?, ?, ?, ?)''',
                   ('Alice', 30, 'New York', 70000))
#Inputting multiple rows of information
employees_data = [
    ('Bob', 25, 'Los Angeles', 60000),
    ('Charlie', 35, 'Chicago', 80000),
    ('David', 28, 'Houston', 65000)]
cursor.executemany('''INSERT INTO employees (
                       name, age, city, salary)
                       VALUES (?, ?, ?, ?)''',
                       employees_data)
connection.commit()
connection.close()
#Querying Data
connection = sqlite3.connect('company.db')
cursor = connection.cursor()
#Querying all employees
cursor.execute('SELECT * FROM employees')
all_data = cursor.fetchall()
print("\n-- All Employees --")
for row in all_data:
    print(row)
#Querying specific columns
cursor.execute('SELECT name, salary FROM employees')
name_salary = cursor.fetchone()
print("\n-- Name and Salary of First Employee --")
print(name_salary)
#Querying with WHERE clause
cursor.execute('SELECT * FROM employees WHERE city = ?',
               ('New York',))
ny_employees = cursor.fetchall()
print("\n-- Employees in New York --")
for row in ny_employees:
    print(row)
#Querying with ORDER BY clause
cursor.execute('SELECT * FROM employees ORDER BY salary DESC')
sorted_employees = cursor.fetchall()
print("\n-- Employees Sorted by Salary (Descending) --")
for row in sorted_employees:
    print(row)
connection.close()
#Row Factory
connection = sqlite3.connect('company.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute('SELECT * FROM employees WHERE salary > ?',
                (65000,))
high_salary_employees = cursor.fetchall()
print("\n-- Employees with Salary Greater than 65000 --")
for row in high_salary_employees:
    print(f"{row['name']} earns ${row['salary']:,.2f}")
connection.close()
#Updating Data
connection = sqlite3.connect('company.db')
cursor = connection.cursor()
#Updating Single Record
cursor.execute('''UPDATE employees
                    SET salary = ?
                    WHERE name = ?''',
                    (75000, 'Alice'))
#Updating Multiple Records
cursor.execute('''UPDATE employees
                    SET salary = salary * 1.10
                    WHERE city = ?''',
                    ('New York',))
#Deleting One Record
cursor.execute('''DELETE FROM employees
                    WHERE name = ?''',
                    ('Bob',))
connection.commit()
cursor.execute('SELECT * FROM employees')
updated_data = cursor.fetchall()
print("\n-- Updated Employees Data --")
for row in updated_data:
    print(row)
connection.close()