import sqlite3, csv
connection = sqlite3.connect('company.db')
cursor = connection.cursor()
with open('employees_clean.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''INSERT INTO employees (name, age, city, salary)
                            VALUES (?,?,?,?)''',
                            (row['name'], int(row['age']), row['city'], float(row['salary'])))
connection.commit()
cursor.execute('SELECT * FROM employees')
all_employees = cursor.fetchall()
print("\n-- All Employees from CSV --")
for employee in all_employees:
    print(employee)
connection.close()