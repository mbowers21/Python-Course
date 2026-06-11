# CSV_Handler.py creates interface between csv files and main software
import csv
from Database import get_all_employees
def export_report(file_name = "report.csv"):
    if not file_name.endswith(".csv"):
        file_name += ".csv"
    employees = get_all_employees()
    if not employees:
        print("No employees found.")
        return
    fieldnames = ["id", "name", "department", "salary"]
    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in employees:
            writer.writerow({k: row[k] for k in fieldnames})
    return file_name
def import_from_csv(file_path):
    if not file_path.endswith(".csv"):
        file_path += ".csv"
    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = row["name"]
                salary = float(row["salary"])
                department_id = int(row["department"]) if row["department"] else 0
                add_employee(name, salary, department_id)
            except (ValueError, KeyError) as e:
                print(f"Error importing row: {e}")