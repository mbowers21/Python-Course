#This is Main.py file for the Company App
#Created by: Matt Bowers (6/10/26)
from Database import (
    get_all_employees,
    get_employee_by_id,
    add_employee,
    initialize_database,
    update_salary,
    delete_employee
)
from CSV_Handler import (
    import_from_csv,
    export_report
)
def show_menu():
    print("\n"+"="*40)
    print("Company Database Manager")
    print("="*40)
    print("1. List All Employees")
    print("2. Find Employee by ID")
    print("3. Add New Employee")
    print("4. Update Employee Salary")
    print("5. Delete Employee")
    print("6. Import from CSV")
    print("7. Export Report to CSV")
    print ("0. Exit")
def main():
    while True:
        show_menu()
        initialize_database()
        choice = input("Enter your choice (0-7): ").strip()
        if choice == '1':
            list_employees()
        elif choice == '2':
            find_employee()
        elif choice == '3':
            add_new_employee()
        elif choice == '4':
            update_employee_salary()
        elif choice == '5':
            delete_employee()
        elif choice == '6':
            import_csv()
        elif choice == '7':
            export_report()
        elif choice == '0':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 7.")

def list_employees():
    employees = get_all_employees()
    if not employees:
        print("No employees found.")
        return
    print("\nAll Employees:")
    print(f"\n{'ID':<5} {'Name':<20} {'Department':<15} {'Salary':>12}")
    print("-"*60)
    for emp in employees:
        dept = emp['department'] if emp['department'] else "No Department"
        print(f"{emp['id']:<5} {emp['name']:<20} {dept:<15} ${emp['salary']:>11.2f}")
def find_employee():
    try:
        emp_id = int(input("Enter Employee ID: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid integer for Employee ID.")
        return
    employee = get_employee_by_id(emp_id)
    if employee:
        dept = employee['department'] if employee['department'] else "No Department"
        print("\nEmployee Details:")
        print(f"ID: {employee['id']}")
        print(f"Name: {employee['name']}")
        print(f"Department: {dept}")
        print(f"Salary: ${employee['salary']:.2f}")
    else:
        print(f"No employee found with ID {emp_id}.")
def add_new_employee():
    print ("\n---Add New Employee---")
    name = input("Enter employee name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    try:
        salary = float(input("Enter employee salary: ").strip())
        department_id = int(input("Enter department ID (or leave blank for no department): ").strip() or 0)
    except ValueError:
        print("Invalid input. \nSalary must be a number. \nDepartment ID must be an integer.")
        return
    try:
        new_id = add_employee(name, salary, department_id)
        print(f"Employee {name} added successfully with ID {new_id}.")
    except Exception as e:
        print(f"Error adding employee: {e}")
def update_employee_salary():
    print("\n---Update Employee Salary---")
    try:
        emp_id = int(input("Enter Employee ID: ").strip())
        new_salary = float(input("Enter new salary: ").strip())
    except ValueError:
        print("Invalid input. \nEmployee ID must be an integer. \nSalary must be a number.")
        return
    try:
        update_salary(emp_id, new_salary)
        print(f"Employee ID {emp_id} salary updated to ${new_salary:.2f}.")
    except Exception as e:
        print(f"Error updating salary: {e}")
def delete_employee():
    print("\n---Delete Employee---")
    try:
        emp_id = int(input("Enter Employee ID: ").strip())
    except ValueError:
        print("Invalid input. Employee ID must be an integer.")
        return
    try:
        delete_employee(emp_id)
        print(f"Employee ID {emp_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting employee: {e}")
def import_csv():
    print("\n---Import from CSV---")
    file_path = input("Enter the path to the CSV file: ").strip()
    try:
        import_from_csv(file_path)
        print("Data imported successfully.")
    except Exception as e:
        print(f"Error importing CSV: {e}")
def export_report():
    print("\n---Export Report to CSV---")
    file_path = input("Enter the path for the output CSV file: ").strip()
    try:
        output_file = export_report(file_path)
        if output_file:
            print(f"Report exported to {output_file}")
        else:
            print("Failed to export report.")
    except Exception as e:
        print(f"Error exporting report: {e}")
if __name__ == "__main__":
    main()