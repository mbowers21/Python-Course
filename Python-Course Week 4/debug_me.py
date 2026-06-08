# debug_me.py
# Week 4 Debugging Exercise
#
# This file connects to company_w4.db — a database with four tables:
#   departments, employees, projects, assignments
#
# It contains SEVEN bugs. Some crash immediately. Others run silently
# but return wrong results. Work top to bottom: fix one bug, re-run,
# then move to the next.
#
# Use the VS Code debugger (Cmd+Shift+D) alongside the procedure document.

import sqlite3, os

DB_PATH = "./company_w4.db"

cwd = os.getcwd()
print(f"Current working directory: {cwd}")
# ── Utility ───────────────────────────────────────────────────────────────────

def get_connection():
    """Return an open connection with row_factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ══════════════════════════════════════════════════════════════════════════════
# Bug 1 — NameError: wrong variable name
# ══════════════════════════════════════════════════════════════════════════════

def get_all_departments():
    """Return every department with its budget and location."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, budget, location FROM departments ORDER BY name")
    departments = cursor.fetchall()
    conn.close()
    return departments            # <-- Bug 1


# ══════════════════════════════════════════════════════════════════════════════
# Bug 2 — Wrong JOIN type: INNER JOIN drops employees with no department
#          Should be LEFT JOIN so contractors show up with NULL dept
# ══════════════════════════════════════════════════════════════════════════════

def get_all_employees_with_dept():
    """
    Return every employee and their department name.
    Employees with no department should show NULL for dept name.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.name        AS employee,
               e.salary,
               e.city,
               d.name        AS department
        FROM   employees e
        LEFT JOIN departments d ON d.id = e.dept_id   -- <-- Bug 2
        ORDER BY e.name
    """)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        dept = row["department"] or "── No Department ──"
        print(f"  {row['employee']:<22} {dept:<22} ${row['salary']:>10,.2f}")
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# Bug 3 — Missing trailing comma in single-value tuple (TypeError)
# ══════════════════════════════════════════════════════════════════════════════

def get_projects_by_status(status):
    """Return all projects with the given status, joined to their department."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name        AS project,
               p.budget,
               p.status,
               d.name        AS department
        FROM   projects p
        LEFT JOIN departments d ON d.id = p.dept_id
        WHERE  p.status = ?
        ORDER BY p.budget DESC
    """, (status,))           # <-- Bug 3
    rows = cursor.fetchall()
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# Bug 4 — Logic error: COUNT(*) counts the NULL row from LEFT JOIN
#          Should be COUNT(e.id) to count only matched employees
# ══════════════════════════════════════════════════════════════════════════════

def get_department_headcount():
    """
    Return every department and how many employees it has.
    Departments with no employees should show 0.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT  d.name          AS department,
                COUNT(*)        AS headcount       -- <-- Bug 4
        FROM    departments d
        LEFT JOIN employees e ON e.dept_id = d.id
        GROUP BY d.id, d.name
        ORDER BY headcount DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# Bug 5 — KeyError: column 'salary' was not included in this SELECT
# ══════════════════════════════════════════════════════════════════════════════

def get_employee_project_summary():
    """
    Return each employee, their department, and every project they are
    assigned to, along with their role and hours on that project.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT  e.name          AS employee,
                d.name          AS department,
                p.name          AS project,
                a.role,
                a.hours
        FROM    assignments a
        INNER JOIN employees   e ON e.id = a.employee_id
        INNER JOIN projects    p ON p.id = a.project_id
        LEFT  JOIN departments d ON d.id = e.dept_id
        ORDER BY e.name, p.name
    """)
    rows = cursor.fetchall()
    conn.close()

    print(f"\n  {'Employee':<22} {'Department':<14} {'Project':<25} {'Role':<14} {'Hrs':>4}")
    print("  " + "-" * 82)
    for row in rows:
        dept = row["department"] or "No Dept"
        print(f"  {row['employee']:<22} {dept:<14} {row['project']:<25} "
              f"{row['role']:<14} {row['hours']:>4}")   # <-- Bug 5


# ══════════════════════════════════════════════════════════════════════════════
# Bug 6 — Missing commit: UPDATE is silently discarded
# ══════════════════════════════════════════════════════════════════════════════

def update_project_status(project_name, new_status):
    """Change the status of a project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE projects SET status = ? WHERE name = ?",
        (new_status, project_name)
    )
    # conn.commit() is missing — change is lost when connection closes
    conn.commit()
    conn.close()
    print(f"  Updated '{project_name}' to {new_status}")


# ══════════════════════════════════════════════════════════════════════════════
# Bug 7 — Infinite loop: loop variable i never increments
# ══════════════════════════════════════════════════════════════════════════════

def total_hours_per_project():
    """
    Sum the hours logged on every project and return a dict
    {project_name: total_hours}.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT  p.name  AS project,
                a.hours
        FROM    assignments a
        INNER JOIN projects p ON p.id = a.project_id
        ORDER BY p.name
    """)
    rows = cursor.fetchall()
    conn.close()

    totals = {}
    i = 0
    while i < len(rows):
        proj  = rows[i]["project"]
        hours = rows[i]["hours"]
        if proj in totals:
            totals[proj] += hours
        else:
            totals[proj] = hours
        
        i += 1  # i never increments — this loops forever      <-- Bug 7
    return totals


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Week 4 Debugging Exercise — debug_me.py")
    print("=" * 60)

    # ── Test 1 ────────────────────────────────────────────────────────────
    print("\n[Test 1] All departments")
    depts = get_all_departments()
    for d in depts:
        print(f"  {d['name']:<15} ${d['budget']:>12,.0f}   {d['location']}")

    # ── Test 2 ────────────────────────────────────────────────────────────
    print("\n[Test 2] All employees with department (including contractors)")
    rows = get_all_employees_with_dept()
    print(f"  Returned {len(rows)} rows  (expected 27 — all employees)")
    for row in rows:
        dept = row["department"] or "── No Department ──"
        print(f"  {row['employee']:<22} {dept:<22} ${row['salary']:>10,.2f}")

    # ── Test 3 ────────────────────────────────────────────────────────────
    print("\n[Test 3] Active projects with their sponsoring department")
    active = get_projects_by_status("Active")
    print(f"  Found {len(active)} active projects  (expected 6)")
    for p in active:
        dept = p["department"] or "No Department"
        print(f"  {p['project']:<26} {dept:<15} ${p['budget']:>10,.0f}   [{p['status']}]")

    # ── Test 4 ────────────────────────────────────────────────────────────
    print("\n[Test 4] Department headcount (Legal should show 0)")
    counts = get_department_headcount()
    for row in counts:
        print(f"  {row['department']:<15} {row['headcount']} employees")
    legal = [r for r in counts if r["department"] == "Legal"]
    print(f"  Legal headcount check: {legal[0]['headcount']}  (expected 0)")

    # ── Test 5 ────────────────────────────────────────────────────────────
    print("\n[Test 5] Employee project assignments (3-table join)")
    get_employee_project_summary()

    # ── Test 6 ────────────────────────────────────────────────────────────
    print("\n[Test 6] Update 'Partner Portal' from On Hold to Active")
    update_project_status("Partner Portal", "Active")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, status FROM projects WHERE name = ?", ("Partner Portal",))
    row = cursor.fetchone()
    conn.close()
    print(f"  Status in DB after update: {row['status']}  (expected Active)")

    # ── Test 7 ────────────────────────────────────────────────────────────
    print("\n[Test 7] Total hours logged per project")
    totals = total_hours_per_project()
    for proj, hrs in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {proj:<26} {hrs:>4} hrs")

    print("\n" + "=" * 60)
    print("  All tests passed — great debugging!")
    print("=" * 60)


if __name__ == "__main__":
    main()
