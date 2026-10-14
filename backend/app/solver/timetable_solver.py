import collections
from ortools.sat.python import cp_model
from typing import List, Dict, Any

class TimetableSolver:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.model = cp_model.CpModel()
        
        self.sections = self.data['sections']
        self.subjects = self.data['subjects']
        self.faculty = self.data.get('faculty', [])
        self.rooms = self.data.get('rooms', [])
        self.assignments = self.data['assignments']
        self.fixed_slots = self.data.get('fixed_slots', [])
        
        self.days = range(5)
        self.periods = range(7)  # Updated to 7 hours per day
        
        # Variables
        self.X = {} # X[section_id, subject_id, day, period]
        self.F = {} # F[section_id, subject_id, day, period, faculty_id]
        self.R = {} # R[section_id, subject_id, day, period, room_id]
        
        self.objective_terms = []
        
    def build_variables(self):
        for assign in self.assignments:
            sec_id = assign['section_id']
            sub_id = assign['subject_id']
            
            for d in self.days:
                for p in self.periods:
                    self.X[(sec_id, sub_id, d, p)] = self.model.NewBoolVar(f'X_{sec_id}_{sub_id}_{d}_{p}')
                    
                    if assign.get('faculty_pool'):
                        for f_id in assign['faculty_pool']:
                            self.F[(sec_id, sub_id, d, p, f_id)] = self.model.NewBoolVar(f'F_{sec_id}_{sub_id}_{d}_{p}_{f_id}')
                            
                    if assign.get('eligible_labs'):
                        for lab in assign['eligible_labs']:
                            r_id = lab['room_id']
                            self.R[(sec_id, sub_id, d, p, r_id)] = self.model.NewBoolVar(f'R_{sec_id}_{sub_id}_{d}_{p}_{r_id}')
        
    def add_hard_constraints(self):
        # 1. Section collision
        for sec in self.sections:
            sec_id = sec['id']
            for d in self.days:
                for p in self.periods:
                    self.model.AddAtMostOne(
                        self.X[(sec_id, assign['subject_id'], d, p)]
                        for assign in self.assignments if assign['section_id'] == sec_id
                    )
        
        # 2. First Hour NEVER Blank (Period 0 must have exactly 1 scheduled class every day for all sections)
        for sec in self.sections:
            sec_id = sec['id']
            sec_assigns = [a for a in self.assignments if a['section_id'] == sec_id]
            for d in self.days:
                self.model.Add(sum(self.X[(sec_id, a['subject_id'], d, 0)] for a in sec_assigns) == 1)

        # 3. Weekly periods & All Lab Hours Continuous in a Single Session per Week
        for assign in self.assignments:
            sec_id = assign['section_id']
            sub_id = assign['subject_id']
            sub = next(s for s in self.subjects if s['id'] == sub_id)
            weekly = sub['weekly_periods']
            
            if sub.get('type') == 'LAB':
                # All weekly lab hours (e.g. 4) must be in ONE single continuous block on ONE day!
                max_start = len(self.periods) - weekly
                possible_starts = list(range(max_start + 1))
                
                Y = {}
                for d in self.days:
                    for start_p in possible_starts:
                        Y[(d, start_p)] = self.model.NewBoolVar(f"Y_{sec_id}_{sub_id}_{d}_{start_p}")
                
                # Exactly 1 continuous session per week
                self.model.Add(sum(Y.values()) == 1)
                
                for d in self.days:
                    for p in self.periods:
                        valid_starts = [sp for sp in possible_starts if sp <= p < sp + weekly]
                        self.model.Add(self.X[(sec_id, sub_id, d, p)] == sum(Y[(d, sp)] for sp in valid_starts))
            else:
                self.model.Add(
                    sum(self.X[(sec_id, sub_id, d, p)] for d in self.days for p in self.periods) 
                    == weekly
                )
            
            # Faculty link
            if assign.get('faculty_pool'):
                req_faculty = assign.get('required_faculty', 1)
                for d in self.days:
                    for p in self.periods:
                        self.model.Add(
                            sum(self.F[(sec_id, sub_id, d, p, f_id)] for f_id in assign['faculty_pool'])
                            == req_faculty * self.X[(sec_id, sub_id, d, p)]
                        )
                        
            # Room link
            if assign.get('eligible_labs'):
                for d in self.days:
                    for p in self.periods:
                        self.model.Add(
                            sum(self.R[(sec_id, sub_id, d, p, lab['room_id'])] for lab in assign['eligible_labs'])
                            == self.X[(sec_id, sub_id, d, p)]
                        )
                        
        # 3. Faculty collision
        for f in self.faculty:
            f_id = f['id']
            for d in self.days:
                for p in self.periods:
                    active_vars = []
                    for assign in self.assignments:
                        if assign.get('faculty_pool') and f_id in assign['faculty_pool']:
                            active_vars.append(self.F[(assign['section_id'], assign['subject_id'], d, p, f_id)])
                    if active_vars:
                        self.model.AddAtMostOne(active_vars)
                        
        # 4. Room collision
        for r in self.rooms:
            r_id = r['id']
            for d in self.days:
                for p in self.periods:
                    active_vars = []
                    for assign in self.assignments:
                        if assign.get('eligible_labs') and any(lab['room_id'] == r_id for lab in assign['eligible_labs']):
                            active_vars.append(self.R[(assign['section_id'], assign['subject_id'], d, p, r_id)])
                    if active_vars:
                        self.model.AddAtMostOne(active_vars)

        # 5. Fixed slots
        for fixed in self.fixed_slots:
            sec_id = fixed['section_id']
            d = fixed['day']
            p = fixed['period']
            sub_id = fixed.get('subject_id')
            if sub_id:
                self.model.Add(self.X[(sec_id, sub_id, d, p)] == 1)
            else:
                for assign in self.assignments:
                    if assign['section_id'] == sec_id:
                        self.model.Add(self.X[(sec_id, assign['subject_id'], d, p)] == 0)
                
        # 6. Faculty unavailability
        for f in self.faculty:
            f_id = f['id']
            unavail = f.get('unavailabilities', [])
            for u in unavail:
                d = u['day']
                p = u['period']
                for assign in self.assignments:
                    if assign.get('faculty_pool') and f_id in assign['faculty_pool']:
                        self.model.Add(self.F[(assign['section_id'], assign['subject_id'], d, p, f_id)] == 0)

        # 7. Balanced Daily Load (Each section must have classes across all working days, including Friday)
        for sec in self.sections:
            sec_id = sec['id']
            sec_assigns = [a for a in self.assignments if a['section_id'] == sec_id]
            for d in self.days:
                day_load = sum(self.X[(sec_id, a['subject_id'], d, p)] for a in sec_assigns for p in self.periods)
                # Every day (including Friday) must have at least 3 periods
                self.model.Add(day_load >= 3)
                # Max 6 periods per day to ensure healthy workload
                self.model.Add(day_load <= 6)

        # 8. Spread Theory subjects across days (avoid dumping hours in a single day)
        for assign in self.assignments:
            sec_id = assign['section_id']
            sub_id = assign['subject_id']
            sub = next(s for s in self.subjects if s['id'] == sub_id)
            for d in self.days:
                day_sub_periods = sum(self.X[(sec_id, sub_id, d, p)] for p in self.periods)
                if sub.get('type') == 'THEORY':
                    max_p = 2 if sub.get('weekly_periods', 0) >= 4 else 1
                    self.model.Add(day_sub_periods <= max_p)

    def add_soft_constraints(self):
        # Prefer priority labs
        for assign in self.assignments:
            sec_id = assign['section_id']
            sub_id = assign['subject_id']
            if assign.get('eligible_labs'):
                for lab in assign['eligible_labs']:
                    r_id = lab['room_id']
                    priority = lab.get('priority', 1)
                    penalty = 0
                    if priority == 2: penalty = 2
                    if priority == 3: penalty = 5
                    
                    if penalty > 0:
                        for d in self.days:
                            for p in self.periods:
                                self.objective_terms.append(penalty * self.R[(sec_id, sub_id, d, p, r_id)])

    def solve(self):
        self.build_variables()
        self.add_hard_constraints()
        self.add_soft_constraints()
        
        if self.objective_terms:
            self.model.Minimize(sum(self.objective_terms))
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.Solve(self.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._extract_solution(solver)
        return None
        
    def _extract_solution(self, solver):
        timetable = []
        for assign in self.assignments:
            sec_id = assign['section_id']
            sub_id = assign['subject_id']
            for d in self.days:
                for p in self.periods:
                    if solver.Value(self.X[(sec_id, sub_id, d, p)]):
                        entry = {
                            "section_id": sec_id,
                            "subject_id": sub_id,
                            "day": d,
                            "period": p,
                            "faculty_ids": [],
                            "room_id": None
                        }
                        if assign.get('faculty_pool'):
                            for f_id in assign['faculty_pool']:
                                if solver.Value(self.F[(sec_id, sub_id, d, p, f_id)]):
                                    entry["faculty_ids"].append(f_id)
                        if assign.get('eligible_labs'):
                            for lab in assign['eligible_labs']:
                                r_id = lab['room_id']
                                if solver.Value(self.R[(sec_id, sub_id, d, p, r_id)]):
                                    entry["room_id"] = r_id
                                    
                        timetable.append(entry)
        return timetable
