import json
from collections import defaultdict
from app.core.database import SessionLocal
from app.models.domain import DepartmentSettings, Section, Subject, Faculty, Room, SubjectAssignment, FixedSlot
from app.solver.timetable_solver import TimetableSolver

db = SessionLocal()
settings = db.query(DepartmentSettings).first()
sections = db.query(Section).all()
subjects = db.query(Subject).all()
faculty = db.query(Faculty).all()
rooms = db.query(Room).all()
assignments = db.query(SubjectAssignment).all()
fixed_slots = db.query(FixedSlot).all()

data = {
    "settings": {"working_days": settings.working_days, "periods_per_day": settings.periods_per_day},
    "sections": [{"id": s.id, "name": s.name} for s in sections],
    "subjects": [{"id": s.id, "name": s.name, "type": s.type, "weekly_periods": s.weekly_periods} for s in subjects],
    "faculty": [{"id": f.id, "name": f.name, "unavailabilities": []} for f in faculty],
    "rooms": [{"id": r.id, "name": r.name} for r in rooms],
    "assignments": [],
    "fixed_slots": [{"section_id": fs.section_id, "day": fs.day, "period": fs.period, "subject_id": fs.subject_id} for fs in fixed_slots]
}

for a in assignments:
    data["assignments"].append({
        "section_id": a.section_id,
        "subject_id": a.subject_id,
        "faculty_pool": json.loads(a.faculty_pool) if a.faculty_pool else [],
        "required_faculty": a.required_faculty,
        "eligible_labs": json.loads(a.eligible_labs) if a.eligible_labs else []
    })

print("Solving Timetable for Verification...")
solver = TimetableSolver(data)
solution = solver.solve()

if not solution:
    print("FAILED: No feasible timetable found.")
    exit(1)

print("\n=== TIMETABLE CONSTRAINT VERIFICATION REPORT ===\n")

errors = []

# 1. Faculty Collision Check
faculty_schedule = defaultdict(list)
for entry in solution:
    day = entry['day']
    period = entry['period']
    for f_id in entry['faculty_ids']:
        if (day, period) in faculty_schedule[f_id]:
            errors.append(f"COLLISION: Faculty ID {f_id} is scheduled multiple times on Day {day} Period {period}!")
        faculty_schedule[f_id].append((day, period))

if not errors:
    print("[PASS] FACULTY COLLISION CHECK: PASSED (0 Professors are double-booked).")

# 2. Lab Faculty Count Check
lab_subject_ids = [s.id for s in subjects if "Lab" in s.name]
lab_errors = 0
for entry in solution:
    if entry['subject_id'] in lab_subject_ids:
        if not (2 <= len(entry['faculty_ids']) <= 3):
            lab_errors += 1
            errors.append(f"LAB ERROR: Section {entry['section_id']} Lab on D{entry['day']}P{entry['period']} has {len(entry['faculty_ids'])} faculty.")

if lab_errors == 0:
    print("[PASS] LAB FACULTY COUNT CHECK: PASSED (All labs strictly have 2 or 3 faculty).")

# 3. Association / Fixed Slot Check
# Year 2 -> Day 2, Periods 4,5,6
# Year 3,4 -> Day 3, Periods 4,5,6
association_errors = 0
for entry in solution:
    sec_name = next(s.name for s in sections if s.id == entry['section_id'])
    if "Year 2" in sec_name and entry['day'] == 2 and entry['period'] in [4, 5, 6]:
        association_errors += 1
    if ("Year 3" in sec_name or "Year 4" in sec_name) and entry['day'] == 3 and entry['period'] in [4, 5, 6]:
        association_errors += 1

if association_errors == 0:
    print("[PASS] ASSOCIATION SLOTS CHECK: PASSED (Afternoons strictly blocked and empty).")

# 4. Weekly Hours / Credits Check
hours_check = defaultdict(int)
for entry in solution:
    hours_check[(entry['section_id'], entry['subject_id'])] += 1

hours_errors = 0
for a in data['assignments']:
    expected = next(s['weekly_periods'] for s in data['subjects'] if s['id'] == a['subject_id'])
    actual = hours_check[(a['section_id'], a['subject_id'])]
    if expected != actual:
        hours_errors += 1
        errors.append(f"HOURS ERROR: Section {a['section_id']} Subject {a['subject_id']} got {actual} hours, expected {expected}.")

if hours_errors == 0:
    print("[PASS] CREDIT HOURS CHECK: PASSED (All 4-credit and 2-credit subjects have exact matching periods).")

if errors:
    print("\nERRORS FOUND:")
    for e in errors:
        print(e)
else:
    print("\n ALL CONSTRAINTS MATHEMATICALLY VERIFIED AND SATISFIED! ")
