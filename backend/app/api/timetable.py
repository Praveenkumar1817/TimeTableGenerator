from fastapi import APIRouter, HTTPException
from app.solver.timetable_solver import TimetableSolver
import json
from app.core.database import SessionLocal
from app.models.domain import DepartmentSettings, Section, Subject, Faculty, Room, SubjectAssignment, FixedSlot

router = APIRouter()

@router.post("/generate")
def generate_timetable():
    db = SessionLocal()
    settings = db.query(DepartmentSettings).first()
    if not settings:
        raise HTTPException(status_code=400, detail="Database not seeded.")
        
    sections = db.query(Section).all()
    subjects = db.query(Subject).all()
    faculty = db.query(Faculty).all()
    rooms = db.query(Room).all()
    assignments = db.query(SubjectAssignment).all()
    fixed_slots = db.query(FixedSlot).all()
    
    data = {
        "settings": {
            "working_days": settings.working_days,
            "periods_per_day": settings.periods_per_day
        },
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
        
    solver = TimetableSolver(data)
    solution = solver.solve()
    
    if solution:
        # Map IDs to names for the UI
        enriched_solution = []
        for entry in solution:
            sec_name = next(s.name for s in sections if s.id == entry['section_id'])
            sub_name = next(s.name for s in subjects if s.id == entry['subject_id'])
            fac_names = [next(f.name for f in faculty if f.id == fid) for fid in entry['faculty_ids']]
            room_name = next(r.name for r in rooms if r.id == entry['room_id']) if entry.get('room_id') else "-"
            
            enriched_solution.append({
                "day": entry['day'],
                "period": entry['period'],
                "section": sec_name,
                "subject": sub_name,
                "faculty": ", ".join(fac_names),
                "room": room_name
            })
            
        # Include all database fixed slots (e.g. Association, Seminar, Sports) dynamically
        for fs in fixed_slots:
            sec_name = next((s.name for s in sections if s.id == fs.section_id), None)
            if sec_name:
                enriched_solution.append({
                    "day": fs.day,
                    "period": fs.period,
                    "section": sec_name,
                    "subject": fs.activity_name or "Association",
                    "faculty": "-",
                    "room": "-"
                })
            
        return {"status": "success", "timetable": enriched_solution}
    else:
        raise HTTPException(status_code=400, detail="No feasible timetable found.")
