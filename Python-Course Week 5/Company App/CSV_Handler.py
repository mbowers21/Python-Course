# CSV_Handler.py creates interface between csv files and main software
import csv
from Database import get_all_employees, get_all_departments, add_department, add_employee
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
    skipped = 0
    imported = 0
    if not file_path.endswith(".csv"):
        file_path += ".csv"
    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        department_map = {row["name"]: row["id"] for row in get_all_departments()}
        for row in reader:
            name = row.get("name", "").strip()
            if not name:
                skipped += 1
                continue
            try:
                name = row["name"]
                salary = float(row["salary"])
                department_id = int(row["department"]) if row["department"] else 0
                add_employee(name, salary, department_id)
            except (ValueError, KeyError) as e:
                skipped += 1
                continue
            department_name = row.get("department", "").strip()
            if department_name and department_name not in department_map:
                new_id = add_department(department_name)
                department_map[department_name] = new_id
            add_employee(name, salary, department_map[department_name])
            imported += 1
    return imported, skipped