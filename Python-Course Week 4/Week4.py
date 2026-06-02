import sqlite3
connection = sqlite3.connect('mydatabase.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS departments
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    location TEXT)
                    ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    department_id INTEGER REFERENCES departments(id),
                    salary REAL)
                    ''')
"""
cursor.execute('''INSERT INTO departments (name, location) VALUES
                    ('HR', 'New York'),
                    ('Engineering', 'San Francisco'),
                    ('Marketing', 'Chicago')
                    ''')
cursor.execute('''INSERT INTO employees (name, department_id, salary) VALUES
                    ('Alice', 1, 60000),
                    ('Bob', 2, 80000),
                    ('Charlie', 3, 50000)
                    ''')
connection.commit()
connection.close()
"""
cursor.execute('''SELECT employees.name, departments.name AS department, employees.salary
                    FROM employees
                    INNER JOIN departments ON employees.department_id = departments.id
                    ORDER BY employees.salary DESC
                ''')
for row in cursor.fetchall():
    print(f"Employee: {row[0]}, Department: {row[1]}, Salary: {row[2]}")
connection.close()

connection = sqlite3.connect('mydatabase.db')
cursor = connection.cursor()
cursor.execute('''SELECT
                    departments.name AS department,
                    COUNT(employees.id) AS employee_count,
                    AVG(employees.salary) AS average_salary,
                    MAX(employees.salary) AS max_salary,
                    MIN(employees.salary) AS min_salary
                FROM departments
                LEFT JOIN employees ON employees.department_id = departments.id
                GROUP BY departments.id
                ORDER BY average_salary DESC
                ''')
for row in cursor.fetchall():
    print(f"Department: {row[0]}, Employee Count: {row[1]}, Average Salary: {row[2]}, Max Salary: {row[3]}, Min Salary: {row[4]}")
connection.close()
#Error Handling
def insert_department(name, location):
    try:
        connection = sqlite3.connect('mydatabase.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO departments (name, location) VALUES (?, ?)''',
                       (name, location))
        connection.commit()
        print(f"Department {name} inserted successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        connection.close()
insert_department('Sales', 'Los Angeles')
insert_department('Marketing', 'Seattle')