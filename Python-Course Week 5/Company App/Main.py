#This is Main.py file for the Company App
#Created by: Matt Bowers (6/10/26)
from typing import Any

from Database import (
    get_all_employees,
    get_employee_by_id,
    add_employee,
    initialize_database,
    update_salary,
    delete_employee,
    get_employees_by_department,
    get_all_departments,
    get_department_by_id,
    add_department,
    update_department_location,
    update_department_name
)
import curses, sqlite3
from CSV_Handler import (
    import_from_csv,
    export_report
)
def run_menu(stdscr, title, options):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    selected_option = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        #Display the Title
        title_text = f"  {title}  "
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(1, 2, title_text)
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(2, 2, "-" * min(len(title_text) + 4, width - 4))
        # Display Menu Items
        for i, option in enumerate(options):
            row = 4 + i
            if row >= height - 2:
                break
            if i == selected_option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(row, 4, f"  {option:<40}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(row, 4, f"  {option:<40}")
        # Footer
        footer = "Use arrow keys to navigate, Enter to select, q to quit"
        stdscr.addstr(height - 1, 2, footer[:width - 3])
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(options)
        elif key in (ord('\n'), curses.KEY_ENTER, ord('\r')):
            return selected_option
        elif key in (ord('q'), ord('Q')):
            return -1
def pause(stdscr, message="Press any key to continue..."):
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height - 1, 2, message[:width - 3])
    stdscr.refresh()
    stdscr.getch()
def input_field(stdscr, prompt, row=10):
    curses.echo()
    curses.curs_set(1)
    stdscr.addstr(row, 4, prompt)
    stdscr.refresh()
    value = stdscr.getstr(row, 4 + len(prompt), 60).decode('utf-8').strip()
    curses.noecho()
    curses.curs_set(0)
    return value
def draw_header(stdscr, title):
    stdscr.clear()
    stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(1, 2, f"  {title}  ")
    stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(2, 2, "-" * (len(title) + 6))
# Set Employee Screens
def screen_list_employees(stdscr):
    draw_header(stdscr, "List All Employees")
    employees = get_all_employees()
    if not employees:
        stdscr.addstr(4, 4, "No employees found.")
        stdscr.refresh()
        pause(stdscr)
        return
    stdscr.addstr(4, 4, f"{'ID':<5} {'Name':<20} {'Department':<15} {'Salary':>12}")
    stdscr.addstr(5, 4, "-" * 60)
    for i, emp in enumerate(employees):
        dept = emp['department'] if emp['department'] else "No Department"
        stdscr.addstr(6 + i, 4, f"{emp['id']:<5} {emp['name']:<20} {dept:<15} ${emp['salary']:>11.2f}")
    stdscr.refresh()
    pause(stdscr)
def screen_find_employee(stdscr):
    draw_header(stdscr, "Find Employee by ID")
    raw = input_field(stdscr, "Employee ID: ", row=4)
    try:
        emp_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Employee ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    employee = get_employee_by_id(emp_id)
    if employee:
        dept = employee['department'] if employee['department'] else "No Department"
        stdscr.addstr(4, 4, f"ID: {employee['id']}")
        stdscr.addstr(5, 4, f"Name: {employee['name']}")
        stdscr.addstr(6, 4, f"Department: {dept}")
        stdscr.addstr(7, 4, f"Salary: ${employee['salary']:.2f}")
    else:
        stdscr.addstr(4, 4, f"No employee found with ID {emp_id}.")
    stdscr.refresh()
    pause(stdscr)
def screen_add_employee(stdscr):
    draw_header(stdscr, "Add New Employee")
    name = input_field(stdscr, "Employee Name: ", row=4)
    if not name:
        stdscr.addstr(4, 4, "Name cannot be empty.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        salary = float(input_field(stdscr, "Employee Salary: ", row=5))
        department_id = int(input_field(stdscr, "Department ID (or 0 for no department): ", row=6))
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter valid numbers.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        new_id = add_employee(name, salary, department_id)
        stdscr.addstr(4, 4, f"Employee {name} added successfully with ID {new_id}.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error adding employee: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_update_employee_salary(stdscr):
    draw_header(stdscr, "Update Employee Salary")
    raw = input_field(stdscr, "Employee ID: ", row=4)
    try:
        emp_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Employee ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    employee = get_employee_by_id(emp_id)
    if not employee:
        stdscr.addstr(4, 4, f"No employee found with ID {emp_id}.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        new_salary = float(input_field(stdscr, "New Salary: ", row=5))
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid number for the new salary.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        update_employee(emp_id, salary=new_salary)
        stdscr.addstr(4, 4, f"Salary for employee {employee['name']} updated successfully.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error updating employee salary: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_import_csv(stdscr):
    draw_header(stdscr, "Import from CSV")
    file_path = input_field(stdscr, "CSV File Path: ", row=4)
    try:
        import_from_csv(file_path)
        stdscr.addstr(4, 4, "Data imported successfully.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error importing CSV: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_export_report(stdscr):
    draw_header(stdscr, "Export Report to CSV")
    file_path = input_field(stdscr, "CSV File Path: ", row=4)
    try:
        export_to_csv(file_path)
        stdscr.addstr(4, 4, "Report exported successfully.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error exporting report: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_delete_employee(stdscr):
    draw_header(stdscr, "Delete Employee")
    raw = input_field(stdscr, "Employee ID: ", row=4)
    try:
        emp_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Employee ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    employee = get_employee_by_id(emp_id)
    if not employee:
        stdscr.addstr(4, 4, f"No employee found with ID {emp_id}.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        delete_employee(emp_id)
        stdscr.addstr(4, 4, f"Employee {employee['name']} deleted successfully.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error deleting employee: {e}")
    stdscr.refresh()
    pause(stdscr)
# Department Screens
def screen_list_departments(stdscr):
    draw_header(stdscr, "List All Departments")
    departments = get_all_departments()
    if not departments:
        stdscr.addstr(4, 4, "No departments found.")
        stdscr.refresh()
        pause(stdscr)
        return
    stdscr.addstr(4, 4, "All Departments:")
    for dept in departments:
        stdscr.addstr(5 + departments.index(dept), 4, f"ID: {dept['id']}, Name: {dept['name']}")
    stdscr.refresh()
    pause(stdscr)
def screen_add_department(stdscr):
    draw_header(stdscr, "Add New Department")
    name = input_field(stdscr, "Department Name: ", row=4)
    if not name:
        stdscr.addstr(4, 4, "Name cannot be empty.")
        stdscr.refresh()
        pause(stdscr)
        return
    location = input_field(stdscr, "Department Location (optional): ", row=5)
    try:
        new_id = add_department(name, location)
        stdscr.addstr(4, 4, f"Department {name} added successfully with ID {new_id}.")
    except sqlite3.IntegrityError:
        stdscr.addstr(4, 4, f"Department {name} already exists.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error adding department: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_rename_department(stdscr):
    draw_header(stdscr, "Rename Department")
    raw = input_field(stdscr, "Department ID: ", row=4)
    try:
        dept_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Department ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    department = get_department_by_id(dept_id)
    if not department:
        stdscr.addstr(4, 4, f"No department found with ID {dept_id}.")
        stdscr.refresh()
        pause(stdscr)
        return
    new_name = input_field(stdscr, "New Department Name: ", row=5)
    if not new_name:
        stdscr.addstr(4, 4, "Name cannot be empty.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        update_department(dept_id, name=new_name)
        stdscr.addstr(4, 4, f"Department {department['name']} renamed to {new_name} successfully.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error renaming department: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_update_department_location(stdscr):
    draw_header(stdscr, "Update Department Location")
    raw = input_field(stdscr, "Department ID: ", row=4)
    try:
        dept_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Department ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    department = get_department_by_id(dept_id)
    if not department:
        stdscr.addstr(4, 4, f"No department found with ID {dept_id}.")
        stdscr.refresh()
        pause(stdscr)
        return
    new_location = input_field(stdscr, "New Department Location: ", row=5)
    if not new_location:
        stdscr.addstr(4, 4, "Location cannot be empty.")
        stdscr.refresh()
        pause(stdscr)
        return
    try:
        update_department(dept_id, location=new_location)
        stdscr.addstr(4, 4, f"Department {department['name']} location updated to {new_location} successfully.")
    except Exception as e:
        stdscr.addstr(4, 4, f"Error updating department location: {e}")
    stdscr.refresh()
    pause(stdscr)
def screen_view_department_employees(stdscr):
    draw_header(stdscr, "View Department Employees")
    raw = input_field(stdscr, "Department ID: ", row=4)
    try:
        dept_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Department ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    department = get_department_by_id(dept_id)
    if not department:
        stdscr.addstr(4, 4, f"No department found with ID {dept_id}.")
        stdscr.refresh()
        pause(stdscr)
        return
    employees = get_employees_by_department(dept_id)
    if not employees:
        stdscr.addstr(4, 4, f"No employees found in department {department['name']}.")
        stdscr.refresh()
        pause(stdscr)
        return
    stdscr.addstr(4, 4, f"Employees in {department['name']}:")
    for emp in employees:
        stdscr.addstr(5 + employees.index(emp), 4, f"ID: {emp['id']}, Name: {emp['name']}, Salary: ${emp['salary']:.2f}")
    stdscr.refresh()
    pause(stdscr)
def screen_delete_department(stdscr):
    draw_header(stdscr, "Delete Department")
    raw = input_field(stdscr, "Department ID: ", row=4)
    try:
        dept_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Department ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    department = get_department_by_id(dept_id)
    if not department:
        stdscr.addstr(4, 4, f"No department found with ID {dept_id}.")
        stdscr.refresh()
        pause(stdscr)
        return
    confirm = input_field(stdscr, f"Are you sure you want to delete {department['name']}? (y/n): ", row=5)
    if confirm.lower() == 'y':
        try:
            delete_department(dept_id)
            stdscr.addstr(4, 4, f"Department {department['name']} deleted successfully.")
        except Exception as e:
            stdscr.addstr(4, 4, f"Error deleting department: {e}")
    else:
        stdscr.addstr(4, 4, "Operation cancelled.")
    stdscr.refresh()
    pause(stdscr)
def screen_find_department(stdscr):
    draw_header(stdscr, "Find Department by ID")
    raw = input_field(stdscr, "Department ID: ", row=4)
    try:
        dept_id = int(raw)
    except ValueError:
        stdscr.addstr(4, 4, "Invalid input. Please enter a valid integer for Department ID.")
        stdscr.refresh()
        pause(stdscr)
        return
    department = get_department_by_id(dept_id)
    if department:
        stdscr.addstr(4, 4, f"Department found: {department['name']}")
    else:
        stdscr.addstr(4, 4, f"No department found with ID {dept_id}.")
    stdscr.refresh()
    pause(stdscr)
#Menus
def departments_menu(stdscr):
    options = [
        "List All Departments",
        "Find Department by ID",
        "Add New Department",
        "Update Department Name",
        "Update Department Location",
        "View Department Employees",
        "Delete Department",
        "Return to Main Menu"
    ]
    actions = [
        screen_list_departments,
        screen_find_department,
        screen_add_department,
        screen_rename_department,
        screen_update_department_location,
        screen_view_department_employees,
        screen_delete_department,
        main_menu,
        lambda stdscr: None
    ]
    while True:
        choice = run_menu(stdscr, "Manage Departments", options=options)
        if 0 <= choice < len(actions):
            actions[choice](stdscr)
        else:
            break
def main_menu(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    options = [
        "List All Employees",
        "Find Employee by ID",
        "Add New Employee",
        "Update Employee Salary",
        "Delete Employee",
        "Manage Departments",
        "Import from CSV",
        "Export Report to CSV",
        "Exit"
    ]
    actions = [
        screen_list_employees,
        screen_find_employee,
        screen_add_employee,
        screen_update_employee_salary,
        screen_delete_employee,
        departments_menu,
        screen_import_csv,
        screen_export_report,
        lambda stdscr: None
    ]
    while True:
        choice = run_menu(stdscr, "Company Database Manager", options=options)
        if 0 <= choice < len(actions):
            actions[choice](stdscr)
        else:
            break
def main():
    initialize_database()
    curses.wrapper(main_menu)
    print("Exiting the program. Goodbye!")
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
if __name_
_ == "__main__":
    main()