#Opening a Text File
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())
#Opening a Text File as a List
with open("data.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())
#Writing to a File
with open("output.txt", "a") as file:
    for i in range(10):
        file.write(f"This is additional line {i+1}\n")
#Using the CSV Processing
import csv
with open("employees.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)
    print(header)
    for row in reader:
        print(row)
#Using the CSV DictReader
with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["name"]
        age = row["age"]
        city = row["city"]
        salary = row["salary"]
        print(f"Name: {name}, Age: {age}, City: {city}, Salary: {salary}")
#Cleaning Up csv Data
cleaned = []
with open("employees.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if not row["name"].strip() or not row["salary"].strip():
            print(f"Skipping incomplete row: {row}")
            continue
        try:
            row["salary"] = float(row["salary"])
        except ValueError:
            print(f"Invalid salary for: {row['name']}")
            continue
        row["city"] = row["city"].strip().title()
        cleaned.append(row)
print(f"Kept {len(cleaned)} valid rows")
#Summarizing Salary Data
salaries = [row["salary"] for row in cleaned]
total = sum(salaries)
average = total / len(salaries)
minimum = min(salaries)
maximum = max(salaries)
print(f"Total Salary: ${total:.2f}")
print(f"Average Salary: ${average:.2f}")
print(f"Minimum Salary: ${minimum:.2f}")
print(f"Maximum Salary: ${maximum:.2f}")
from collections import defaultdict
city_salaries = defaultdict(list)
for row in cleaned:
    city_salaries[row["city"]].append(row["salary"])
print("\n--Salary by City--")
for city, salaries in city_salaries.items():
    city_average = sum(salaries) / len(salaries)
    print(f"{city}: Average Salary: ${city_average:.2f}")
#Create a New Clean CSV File
with open("employees_clean.csv", "w", newline="") as file:
    fieldnames = ["name", "age", "city", "salary"]
    writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in clean_rows:
        writer.writerow(row)
print("Cleaned data written to employees_clean.csv")