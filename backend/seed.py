import json
from app.core.database import SessionLocal, Base, engine
from app.models.domain import AcademicYear, Section, Subject, Faculty, Room, SubjectAssignment, FixedSlot, DepartmentSettings, SubjectType

def seed_database():
    """
    Seeds the academic timetable database with realistic departmental data:
    - Department Settings (5 working days, 7 periods per day)
    - 6 Lecture Classrooms & 5 Specialized Engineering Laboratories
    - 25 Faculty Members with department affiliations
    - 3 Academic Years (Year 2, Year 3, Year 4) across 6 Sections (Sec A & Sec B)
    - Complete Curriculum with Theory (3-4 periods/week) & Labs (3 continuous periods/week)
    - Faculty subject assignments & multi-faculty lab allocations (2-3 faculty per lab)
    - Department Association Fixed Slots
    """
    print("Initializing database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("Seeding department settings...")
        db.add(DepartmentSettings(working_days=5, periods_per_day=7))

        # 6 Classrooms + 5 Specialised Labs
        print("Seeding rooms & laboratories...")
        classrooms = [
            Room(name="Lecture Hall 201 (LH-201)"),
            Room(name="Lecture Hall 202 (LH-202)"),
            Room(name="Lecture Hall 301 (LH-301)"),
            Room(name="Lecture Hall 302 (LH-302)"),
            Room(name="Lecture Hall 401 (LH-401)"),
            Room(name="Lecture Hall 402 (LH-402)")
        ]
        labs = [
            Room(name="Software Systems Lab (L108)", is_lab=True),
            Room(name="Networks & Systems Lab (IT443)", is_lab=True),
            Room(name="AI & High Performance Lab", is_lab=True),
            Room(name="Hardware & Microprocessors Lab (L204)", is_lab=True),
            Room(name="Cloud & Embedded Systems Lab (L205)", is_lab=True)
        ]
        db.add_all(classrooms + labs)
        db.commit()

        # Faculty (25 members)
        print("Seeding faculty members...")
        faculty_names = [
            "Dr. Rajesh Kannan (HOD)", "Dr. Ananya Sharma", "Dr. Meenakshi Sundaram", "Dr. Arvind Swamy",
            "Dr. Suresh Venkatesh", "Dr. Preethi Ranganathan", "Prof. Karthikeyan M", "Prof. Deepa Balasubramanian",
            "Prof. Vignesh Kumar", "Prof. Sangeetha Ramani", "Prof. Naveen Chandran", "Prof. Priya Dharshini",
            "Prof. Arun Prakash", "Prof. Divya Bharathi", "Prof. Saravanan K", "Prof. Harish Raghavan",
            "Prof. Nithya Kalyani", "Prof. Madhan Mohan", "Prof. Shweta Iyer", "Prof. Anand Babu",
            "Prof. Revathi Narayanan", "Prof. Gokul Krishnan", "Prof. Pavithra S", "Prof. Manoj Prabhakar", "Prof. Uma Maheshwari"
        ]
        faculty_members = [Faculty(name=name) for name in faculty_names]
        db.add_all(faculty_members)
        db.commit()

        # Years & Sections
        print("Seeding academic years & sections...")
        years = [AcademicYear(name="Year 2"), AcademicYear(name="Year 3"), AcademicYear(name="Year 4")]
        db.add_all(years)
        db.commit()

        sections = []
        for y in years:
            sections.append(Section(name=f"{y.name} - Sec A", academic_year_id=y.id))
            sections.append(Section(name=f"{y.name} - Sec B", academic_year_id=y.id))
        db.add_all(sections)
        db.commit()

        curriculum_by_year = {
            "Year 2": {
                "theories": [
                    ("Data Structures & Algorithms", 4),
                    ("Discrete Mathematics", 3),
                    ("Digital Logic & System Design", 3),
                    ("Object-Oriented Programming (Java)", 3),
                    ("Computer Architecture & Organization", 3)
                ],
                "labs": [
                    ("Data Structures Laboratory", 3),
                    ("Java & OOP Laboratory", 3),
                    ("Digital Electronics & Systems Lab", 3)
                ]
            },
            "Year 3": {
                "theories": [
                    ("Database Management Systems", 4),
                    ("Operating Systems & Linux Kernel", 3),
                    ("Computer Networks & Protocols", 3),
                    ("Theory of Computation & Automata", 3),
                    ("Web Technology & Frameworks", 3)
                ],
                "labs": [
                    ("Database Management Systems Lab", 3),
                    ("Operating Systems & Shell Scripting Lab", 3),
                    ("Full-Stack Web Development Lab", 3)
                ]
            },
            "Year 4": {
                "theories": [
                    ("Artificial Intelligence & Machine Learning", 4),
                    ("Cloud Computing & DevOps", 3),
                    ("Cryptography & Network Security", 3),
                    ("Internet of Things & Embedded Systems", 3),
                    ("Mobile Application Development", 3)
                ],
                "labs": [
                    ("AI & Deep Learning Laboratory", 3),
                    ("Cloud Deployment & Security Lab", 3),
                    ("Mobile Apps & IoT Laboratory", 3)
                ]
            }
        }

        print("Seeding curriculum, subjects, and assignments...")
        fac_idx = 0
        lab_room_idx = 0
        for sec in sections:
            year_key = "Year 2" if "Year 2" in sec.name else ("Year 3" if "Year 3" in sec.name else "Year 4")
            curr = curriculum_by_year[year_key]
            
            sec_theories = []
            for sub_name, periods in curr["theories"]:
                sub = Subject(name=sub_name, type=SubjectType.THEORY, weekly_periods=periods)
                db.add(sub)
                sec_theories.append(sub)
            
            sec_labs = []
            for lab_name, periods in curr["labs"]:
                lab = Subject(name=lab_name, type=SubjectType.LAB, weekly_periods=periods)
                db.add(lab)
                sec_labs.append(lab)
                
            db.commit()
            
            for theory in sec_theories:
                f = faculty_members[fac_idx % len(faculty_members)]
                db.add(SubjectAssignment(
                    section_id=sec.id, subject_id=theory.id,
                    faculty_pool=json.dumps([f.id]), required_faculty=1
                ))
                fac_idx += 1
                
            for i, lab in enumerate(sec_labs):
                lab_faculty_count = 3 if i == 0 else 2
                pool = [faculty_members[(fac_idx + k) % len(faculty_members)].id for k in range(lab_faculty_count)]
                fac_idx += lab_faculty_count
                
                assigned_room = labs[lab_room_idx % len(labs)]
                lab_room_idx += 1
                
                db.add(SubjectAssignment(
                    section_id=sec.id, subject_id=lab.id,
                    faculty_pool=json.dumps(pool), required_faculty=lab_faculty_count,
                    eligible_labs=json.dumps([{"room_id": assigned_room.id, "priority": 1}])
                ))

        print("Seeding Association Fixed Slots...")
        for sec in sections:
            if "Year 2" in sec.name:
                for p in [4, 5, 6]:
                    db.add(FixedSlot(section_id=sec.id, day=2, period=p, activity_name="Association"))
            else:
                for p in [4, 5, 6]:
                    db.add(FixedSlot(section_id=sec.id, day=3, period=p, activity_name="Association"))

        db.commit()
        print("Database successfully seeded with full academic departmental dataset!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
