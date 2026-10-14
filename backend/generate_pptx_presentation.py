import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
BG_DARK = RGBColor(15, 23, 42)      # Slate 900
BG_CARD = RGBColor(248, 250, 252)   # Slate 50
TEXT_DARK = RGBColor(30, 41, 59)    # Slate 800
TEXT_MUTED = RGBColor(100, 116, 139)# Slate 500
TEXT_LIGHT = RGBColor(255, 255, 255)# White
ACCENT_BLUE = RGBColor(79, 70, 229) # Indigo 600
ACCENT_TEAL = RGBColor(13, 148, 136)# Teal 600
ACCENT_GREEN = RGBColor(5, 150, 105)# Emerald 600
ACCENT_PURPLE = RGBColor(147, 51, 234) # Purple 600
BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200

blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="MICRO PROJECT PRESENTATION"):
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_BLUE

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_DARK

def create_card(slide, left, top, width, height, bg_color=BG_CARD, border_color=BORDER_COLOR):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape

# ==================== SLIDE 1: TITLE SLIDE ====================
slide1 = prs.slides.add_slide(blank_layout)
# Dark background
bg_rect = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg_rect.fill.solid()
bg_rect.fill.fore_color.rgb = BG_DARK
bg_rect.line.fill.background()

# Title box
tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.33), Inches(2.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "A MICRO PROJECT DEMONSTRATION & TECHNICAL REPORT"
p_sub.font.size = Pt(13)
p_sub.font.bold = True
p_sub.font.color.rgb = RGBColor(129, 140, 248) # Indigo 400

p_title = tf1.add_paragraph()
p_title.text = "AI-Based Automated College Timetable Generation & Constraint Optimization System"
p_title.font.size = Pt(30)
p_title.font.bold = True
p_title.font.color.rgb = TEXT_LIGHT
p_title.space_before = Pt(10)

p_tag = tf1.add_paragraph()
p_tag.text = "Powered by Google OR-Tools CP-SAT, Python FastAPI, and React/Tailwind CSS"
p_tag.font.size = Pt(15)
p_tag.font.color.rgb = RGBColor(203, 213, 225) # Slate 300
p_tag.space_before = Pt(10)

# Authors Card
auth_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.3), Inches(5.4), Inches(2.3))
auth_card.fill.solid()
auth_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
auth_card.line.color.rgb = RGBColor(51, 65, 85)
tf_ac = auth_card.text_frame
tf_ac.word_wrap = True
tf_ac.margin_left = Inches(0.3)
tf_ac.margin_top = Inches(0.25)

p = tf_ac.paragraphs[0]
p.text = "PROJECT CANDIDATES"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = RGBColor(148, 163, 184)

p2 = tf_ac.add_paragraph()
p2.text = "• SOWNDARIYA R  (Reg. No: 2303717610422123)"
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = TEXT_LIGHT
p2.space_before = Pt(8)

p3 = tf_ac.add_paragraph()
p3.text = "• PRAVEENKUMAR B  (Reg. No: 2303717610421108)"
p3.font.size = Pt(13)
p3.font.bold = True
p3.font.color.rgb = TEXT_LIGHT
p3.space_before = Pt(6)

p4 = tf_ac.add_paragraph()
p4.text = "Bachelor of Engineering in Computer Science and Engineering"
p4.font.size = Pt(11)
p4.font.italic = True
p4.font.color.rgb = RGBColor(148, 163, 184)
p4.space_before = Pt(10)

# Institution Card
inst_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.5), Inches(2.3))
inst_card.fill.solid()
inst_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
inst_card.line.color.rgb = RGBColor(51, 65, 85)
tf_ic = inst_card.text_frame
tf_ic.word_wrap = True
tf_ic.margin_left = Inches(0.3)
tf_ic.margin_top = Inches(0.25)

p = tf_ic.paragraphs[0]
p.text = "INSTITUTION DETAILS"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = RGBColor(148, 163, 184)

p2 = tf_ic.add_paragraph()
p2.text = "COIMBATORE INSTITUTE OF TECHNOLOGY"
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = TEXT_LIGHT
p2.space_before = Pt(8)

p3 = tf_ic.add_paragraph()
p3.text = "Government Aided Autonomous Institution Affiliated to Anna University"
p3.font.size = Pt(11)
p3.font.color.rgb = RGBColor(203, 213, 225)
p3.space_before = Pt(4)

p4 = tf_ic.add_paragraph()
p4.text = "Coimbatore - 641014 | Anna University: Chennai 600 025\nOctober 2026"
p4.font.size = Pt(11)
p4.font.bold = True
p4.font.color.rgb = RGBColor(129, 140, 248)
p4.space_before = Pt(8)

# ==================== SLIDE 2: PROBLEM STATEMENT ====================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Problem Context & Operational Challenges", "BACKGROUND & MOTIVATION")

cards_s2 = [
    ("The NP-Hard Challenge", "Academic timetabling belongs to the NP-hard University Course Timetabling Problem (UCTP). As constraints increase, the search space grows exponentially.", Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), ACCENT_BLUE),
    ("Manual Scheduling Bottlenecks", "Manual compilation takes days of committee meetings, frequently resulting in accidental faculty overlaps, room conflicts, and irregular workload distribution.", Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), RGBColor(225, 29, 72)),
    ("Rigid Collegiate Constraints", "Engineering colleges enforce complex departmental rules: multi-instructor practicals, 3-hour unbroken labs, association afternoon locks, and non-empty morning hours.", Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), ACCENT_TEAL)
]

for title, desc, l, t, w, h, acc in cards_s2:
    card = create_card(slide2, l, t, w, h)
    tf = card.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.3)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = acc
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(13)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(16)
    
    p3 = tf.add_paragraph()
    p3.text = "Impact: Human error causes student disruption and administrative delay."
    p3.font.size = Pt(11)
    p3.font.italic = True
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(20)

# ==================== SLIDE 3: PROJECT OBJECTIVES ====================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Core Objectives & Project Scope", "SYSTEM GOALS")

objs = [
    ("1. Exact Mathematical Modeling", "Formulate course timetabling as an exact Constraint Satisfaction Problem (CSP) solvable via Google OR-Tools CP-SAT without heuristic approximations."),
    ("2. Zero Clash Guarantee", "Eliminate all teacher double-booking, student cohort clashes, and laboratory venue conflicts across the entire institution."),
    ("3. Unbroken 3-Hour Labs", "Guarantee all practical laboratory courses run as single continuous 3-hour sessions on a single day, strictly respecting lunch and tea breaks."),
    ("4. Non-Empty Period 1 (Morning Rule)", "Ensure the first period of every working day is actively scheduled across all sections to eliminate idle morning hours."),
    ("5. Multi-Faculty Lab Staffing", "Simultaneously co-allocate 2 to 3 instructors to each laboratory session based on institutional lab staffing quotas."),
    ("6. Enterprise Web Experience", "Deliver a responsive React/Tailwind CSS dashboard with section-grouped curriculum management, focus modals, and one-click PDF/CSV export.")
]

for i, (title, text) in enumerate(objs):
    col = i % 2
    row = i // 2
    l = Inches(0.8 + col * 5.9)
    t = Inches(1.7 + row * 1.7)
    w = Inches(5.6)
    h = Inches(1.5)
    
    card = create_card(slide3, l, t, w, h)
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = text
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(6)

# ==================== SLIDE 4: SYSTEM ARCHITECTURE ====================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Three-Tier Modern System Architecture", "SYSTEM ARCHITECTURE")

tiers = [
    ("PRESENTATION TIER", "React 18 + TypeScript + Vite + Tailwind CSS", [
        "Interactive 7-period collegiate timetable grids",
        "Section Focus Modal for high-legibility viewing",
        "Section-grouped curriculum & assignment managers",
        "Client-side RFC 4180 CSV & @media print PDF export"
    ], Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), ACCENT_BLUE),
    ("APPLICATION TIER", "Python FastAPI RESTful Backend Engine", [
        "High-performance asynchronous endpoints",
        "CRUD routers for sections, courses, faculty, and rooms",
        "Pydantic data contracts with optional typing",
        "Payload assembler for solver handoff & solution enrichment"
    ], Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), ACCENT_PURPLE),
    ("OPTIMIZATION & DATA", "Google OR-Tools CP-SAT + SQLAlchemy ORM", [
        "Boolean Satisfiability decision variables (X, F, R, Y)",
        "Hard collision, continuity, and morning bounds",
        "SQLite relational database (timetable.db)",
        "Swappable to PostgreSQL/MySQL via database URL"
    ], Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), ACCENT_TEAL)
]

for title, sub, bullets, l, t, w, h, acc in tiers:
    card = create_card(slide4, l, t, w, h)
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = acc
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(4)
    
    for b in bullets:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_DARK
        pb.space_before = Pt(8)

# ==================== SLIDE 5: AI OPTIMIZATION ENGINE ====================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Google OR-Tools CP-SAT Optimization Engine", "AI ALGORITHMIC FORMULATION")

card_left = create_card(slide5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf_l = card_left.text_frame
tf_l.margin_left = Inches(0.3)
tf_l.margin_top = Inches(0.25)
tf_l.word_wrap = True

p = tf_l.paragraphs[0]
p.text = "Mathematical Decision Variables"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p2 = tf_l.add_paragraph()
p2.text = "• X[s, c, d, p] ∈ {0, 1} : Section s attends course c on day d at period p."
p2.font.size = Pt(12)
p2.font.color.rgb = TEXT_DARK
p2.space_before = Pt(12)

p3 = tf_l.add_paragraph()
p3.text = "• F[s, c, d, p, f] ∈ {0, 1} : Faculty f teaches course c to section s at (d, p)."
p3.font.size = Pt(12)
p3.font.color.rgb = TEXT_DARK
p3.space_before = Pt(10)

p4 = tf_l.add_paragraph()
p4.text = "• R[s, c, d, p, r] ∈ {0, 1} : Lab room r hosts course c for section s at (d, p)."
p4.font.size = Pt(12)
p4.font.color.rgb = TEXT_DARK
p4.space_before = Pt(10)

p5 = tf_l.add_paragraph()
p5.text = "• Y[s, c, d, p_start] ∈ {0, 1} : Single 3-hour continuous lab session starts at period p_start on day d."
p5.font.size = Pt(12)
p5.font.color.rgb = TEXT_DARK
p5.space_before = Pt(10)

card_right = create_card(slide5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
tf_r = card_right.text_frame
tf_r.margin_left = Inches(0.3)
tf_r.margin_top = Inches(0.25)
tf_r.word_wrap = True

p = tf_r.paragraphs[0]
p.text = "Mathematical Hard Constraints"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN

rules = [
    "1. Section Clash Limit: ∑ c X[s, c, d, p] ≤ 1",
    "2. Non-Empty Period 1: ∑ c X[s, c, d, 0] = 1 (Every day starts with active class)",
    "3. Contiguous 3-Hour Labs: ∑ d,p Y[s,c,d,p] = 1 (All 3h scheduled in 1 session)",
    "4. Multi-Faculty Lab Pool: ∑ f F[s, c, d, p, f] = M · X[s, c, d, p] (M ∈ {2, 3})",
    "5. Faculty Clash Limit: ∑ s,c F[s, c, d, p, f] ≤ 1 (No teacher overlaps)",
    "6. Room Clash Limit: ∑ s,c R[s, c, d, p, r] ≤ 1 (No venue overlaps)",
    "7. Association Lockout: X[s, c, d_assoc, p_assoc] = 0 (Wed / Thu afternoons)"
]

for r in rules:
    pr = tf_r.add_paragraph()
    pr.text = r
    pr.font.size = Pt(11.5)
    pr.font.color.rgb = TEXT_DARK
    pr.space_before = Pt(8)

# ==================== SLIDE 6: LABORATORY & MULTI-FACULTY LOGIC ====================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Unbroken 3-Hour Labs & Multi-Faculty Staffing", "LABORATORY & STAFFING CONSTRAINTS")

c1 = create_card(slide6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
tf1 = c1.text_frame
tf1.margin_left = Inches(0.3)
tf1.margin_top = Inches(0.25)
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "Contiguous 3-Hour Lab Block Rule"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

pts1 = [
    "All 3 lab hours must be conducted in ONE continuous single session on the same day.",
    "Eliminated midday fragmentation: practicals never split into isolated 1-hour or 2-hour slots.",
    "Respects institutional rest intervals: labs do not unergonomically cross Lunch.",
    "Permissible start periods: P0 (Morning P1-P3) or P4 (Afternoon P5-P7)."
]
for pt in pts1:
    pr = tf1.add_paragraph()
    pr.text = "• " + pt
    pr.font.size = Pt(12)
    pr.font.color.rgb = TEXT_DARK
    pr.space_before = Pt(12)

c2 = create_card(slide6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
tf2 = c2.text_frame
tf2.margin_left = Inches(0.3)
tf2.margin_top = Inches(0.25)
tf2.word_wrap = True

p = tf2.paragraphs[0]
p.text = "Multi-Faculty Laboratory Pools"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = ACCENT_PURPLE

pts2 = [
    "Practical courses enforce 2 or 3 faculty members co-assigned simultaneously.",
    "High student-to-faculty lab ratio compliance as mandated by accreditation norms (NBA/AICTE).",
    "The solver synchronizes instructors so neither teacher is double-booked in another lecture hall.",
    "Verified: 18 out of 18 lab sessions strictly staffed by 2 to 3 instructors simultaneously."
]
for pt in pts2:
    pr = tf2.add_paragraph()
    pr.text = "• " + pt
    pr.font.size = Pt(12)
    pr.font.color.rgb = TEXT_DARK
    pr.space_before = Pt(12)

# ==================== SLIDE 7: RELATIONAL DATABASE & DOMAIN ====================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Relational Schema & Dynamic Persistence", "DATABASE ARCHITECTURE")

db_tables = [
    ("sections", "Section ID, Name ('Year 2 - Sec A'), Academic Year Foreign Key", Inches(0.8), Inches(1.8)),
    ("subjects", "Subject ID, Course Name, Classification (THEORY/LAB), Weekly Hours (3-4h)", Inches(6.8), Inches(1.8)),
    ("faculty", "Faculty ID, Full Academic Name ('Dr. Rajesh Kannan (HOD)'), Unavailabilities", Inches(0.8), Inches(3.4)),
    ("rooms", "Room ID, Venue Name ('LH-201', 'L108 Lab'), Lab Boolean Flag, Capacity", Inches(6.8), Inches(3.4)),
    ("subject_assignments", "Section ID, Subject ID, Required Faculty Count, Faculty Pool JSON, Eligible Labs JSON", Inches(0.8), Inches(5.0)),
    ("fixed_slots", "Section ID, Day Index, Period Index, Reserved Activity Label ('Association')", Inches(6.8), Inches(5.0))
]

for name, desc, l, t in db_tables:
    card = create_card(slide7, l, t, Inches(5.7), Inches(1.3))
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.18)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "TABLE: " + name
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(4)

# ==================== SLIDE 8: USER INTERFACE WALKTHROUGH ====================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Modern Administrative UI & Collegiate Grids", "USER INTERFACE WALKTHROUGH")

ui_feats = [
    ("Collegiate Timetable Grid", "Renders 7 periods per day with distinct Break and Lunch dividers. Table-fixed proportions ensure no horizontal sliding on standard desktop displays.", Inches(0.8), Inches(1.8), ACCENT_BLUE),
    ("Expand Focus Modal", "One-click 'Expand View' opens a spacious, large-typography modal view for single-section inspection, complete with dedicated single-page printing.", Inches(4.8), Inches(1.8), ACCENT_PURPLE),
    ("Section-Grouped Curriculum", "Subjects and assignments are structured directly under their respective cohorts, displaying weekly hours, instructor pools, and lab venue badges.", Inches(8.8), Inches(1.8), ACCENT_GREEN),
    ("Dynamic CRUD Management", "Intuitive forms for adding/deleting instructors, sections, and courses with immediate backend cascade integrity.", Inches(0.8), Inches(4.5), RGBColor(217, 119, 6)),
    ("Export & Documentation", "Instant client-side RFC 4180 CSV export and CSS paged media (@media print) for high-resolution PDF outputs.", Inches(4.8), Inches(4.5), ACCENT_TEAL),
    ("Real-Time Status & Errors", "Instant visual feedback displaying solver convergence status and helpful error modals if constraints conflict.", Inches(8.8), Inches(4.5), RGBColor(225, 29, 72))
]

for title, desc, l, t, acc in ui_feats:
    card = create_card(slide8, l, t, Inches(3.7), Inches(2.3))
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = acc
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(8)

# ==================== SLIDE 9: BENCHMARK & PERFORMANCE ====================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Empirical Benchmark & Verification Results", "PERFORMANCE & BENCHMARKS")

bench_stats = [
    ("0.84 s", "CP-SAT Solver Runtime", "Sub-second convergence to optimal solution", ACCENT_BLUE),
    ("100%", "Constraint Satisfaction", "Zero faculty, cohort, or room collisions", ACCENT_GREEN),
    ("100%", "Period 1 Occupancy", "All 30 section-days start with active class", ACCENT_PURPLE),
    ("18 / 18", "Continuous 3-Hour Labs", "100% of practicals unbroken single sessions", ACCENT_TEAL)
]

for i, (metric, label, desc, acc) in enumerate(bench_stats):
    l = Inches(0.8 + i * 2.95)
    card = create_card(slide9, l, Inches(1.8), Inches(2.8), Inches(1.8))
    tf = card.text_frame
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = metric
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = acc
    
    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = TEXT_MUTED

card_bot = create_card(slide9, Inches(0.8), Inches(3.9), Inches(11.7), Inches(2.8))
tf_b = card_bot.text_frame
tf_b.margin_left = Inches(0.3)
tf_b.margin_top = Inches(0.25)
tf_b.word_wrap = True

p = tf_b.paragraphs[0]
p.text = "Departmental Benchmark Parameters Evaluated"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = TEXT_DARK

details = [
    "• Scope: 3 Academic Years (Years 2, 3, 4) × 2 Sections each = 6 Student Sections.",
    "• Course Catalog: 48 Subjects (24 Theory courses @ 3-4 credits, 24 Practical Laboratories @ 3 credits).",
    "• Infrastructure: 11 Total Venues (6 Lecture Halls + 5 Specialized Computing & Hardware Labs).",
    "• Faculty Staffing: 25 Distinguished Professors (including HOD), co-teaching labs in pools of 2 or 3.",
    "• Total Demand: 144 Weekly class periods assigned with 100% demand satisfaction."
]

for d in details:
    pr = tf_b.add_paragraph()
    pr.text = d
    pr.font.size = Pt(11)
    pr.font.color.rgb = TEXT_DARK
    pr.space_before = Pt(4)

# ==================== SLIDE 10: WEEKLY SCHEDULE DISTRIBUTION ====================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Balanced Daily Distribution & Full Friday Coverage", "WORKLOAD DISTRIBUTION")

dist_data = [
    ("Year 2 - Section A", "Mon: 5h | Tue: 6h | Wed: 4h (+Assn) | Thu: 5h | Fri: 5h", "25 Contact Hours", ACCENT_BLUE),
    ("Year 2 - Section B", "Mon: 5h | Tue: 5h | Wed: 4h (+Assn) | Thu: 6h | Fri: 5h", "25 Contact Hours", ACCENT_BLUE),
    ("Year 3 - Section A", "Mon: 5h | Tue: 6h | Wed: 5h | Thu: 4h (+Assn) | Fri: 5h", "25 Contact Hours", ACCENT_PURPLE),
    ("Year 3 - Section B", "Mon: 6h | Tue: 5h | Wed: 5h | Thu: 4h (+Assn) | Fri: 5h", "25 Contact Hours", ACCENT_PURPLE),
    ("Year 4 - Section A", "Mon: 5h | Tue: 5h | Wed: 6h | Thu: 4h (+Assn) | Fri: 5h", "25 Contact Hours", ACCENT_TEAL),
    ("Year 4 - Section B", "Mon: 5h | Tue: 6h | Wed: 5h | Thu: 4h (+Assn) | Fri: 5h", "25 Contact Hours", ACCENT_TEAL)
]

for i, (sec, schedule, total, acc) in enumerate(dist_data):
    l = Inches(0.8 if i % 2 == 0 else 6.8)
    t = Inches(1.8 + (i // 2) * 1.6)
    card = create_card(slide10, l, t, Inches(5.7), Inches(1.4))
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.18)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = sec + f"  ({total})"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = acc
    
    p2 = tf.add_paragraph()
    p2.text = schedule
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(6)

# ==================== SLIDE 11: CP-SAT VS HEURISTICS ====================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Algorithmic Comparison: Why CP-SAT Wins", "ALGORITHMIC COMPARISON")

comps = [
    ("MANUAL SCHEDULING", "Human Timetable Committees", [
        "Days of tedious trial and error",
        "Prone to double-booking and room clashes",
        "Sub-optimal room & lab utilization",
        "Fragile to faculty leave or curriculum changes",
        "Zero mathematical optimality guarantee"
    ], Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), RGBColor(225, 29, 72)),
    ("GENETIC ALGORITHMS", "Heuristic Evolutionary Search", [
        "Stochastic (randomized) convergence",
        "Prone to getting stuck in local minima",
        "High runtime (minutes to hours)",
        "May produce subtle constraint violations",
        "Hard to enforce strict multi-faculty locks"
    ], Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), RGBColor(217, 119, 6)),
    ("CP-SAT (OUR SOLUTION)", "Boolean Satisfiability (SAT / CSP)", [
        "Sub-second convergence (0.84 seconds)",
        "100% mathematical constraint satisfaction",
        "Exact branch-and-bound bound pruning",
        "Guaranteed collision-free feasible schedules",
        "Deterministically testable & verifiable"
    ], Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), ACCENT_GREEN)
]

for title, sub, bullets, l, t, w, h, acc in comps:
    card = create_card(slide11, l, t, w, h)
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = acc
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(4)
    
    for b in bullets:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_DARK
        pb.space_before = Pt(8)

# ==================== SLIDE 12: FUTURE SCOPE ====================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "Future Scope & Platform Extensions", "FUTURE WORK")

futures = [
    ("Soft Faculty Preference Penalties", "Introduce objective weights reflecting individual instructor preferences (e.g. morning vs. afternoon teaching preferences) to optimize faculty satisfaction.", Inches(0.8), Inches(1.8)),
    ("Inter-Departmental Open Electives", "Incorporate multi-commodity flow constraints to support open elective courses attended concurrently by students across multiple departments.", Inches(6.8), Inches(1.8)),
    ("Dynamic Substitute Faculty Recommender", "Integrate an automated schedule repair engine to recommend temporary substitute faculty when an instructor takes unexpected leave.", Inches(0.8), Inches(3.6)),
    ("Bi-Directional Calendar Integration", "Export generated schedules directly to Google Calendar, Microsoft Outlook, and university ERP systems via iCal / REST APIs.", Inches(6.8), Inches(3.6)),
    ("Multi-Campus Logistics Management", "Model travel-time buffer constraints for faculty commuting between multiple academic campuses or distributed university buildings.", Inches(0.8), Inches(5.4)),
    ("Student Attendance & Feedback Integration", "Link classroom allocations to historical student batch attendance data for real-time room capacity sizing.", Inches(6.8), Inches(5.4))
]

for title, desc, l, t in futures:
    card = create_card(slide12, l, t, Inches(5.7), Inches(1.5))
    tf = card.text_frame
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(4)

# ==================== SLIDE 13: CONCLUSION ====================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "Conclusion & Project Summary", "CONCLUSION")

c_sum = create_card(slide13, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
tf_s = c_sum.text_frame
tf_s.margin_left = Inches(0.35)
tf_s.margin_top = Inches(0.3)
tf_s.word_wrap = True

p = tf_s.paragraphs[0]
p.text = "Key Project Takeaways"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

concls = [
    "Proven Mathematical Optimality: Successfully transitioned college timetable scheduling from trial-and-error manual compilation to exact CP-SAT constraint satisfaction.",
    "Instantaneous Execution: Solved complex 6-section curriculum across 48 courses, 25 professors, and 11 venues in under 1 second (0.84s).",
    "Strict Collegiate Rule Compliance: Achieved 100% adherence to 3-hour unbroken laboratory sessions, Period 1 morning occupancy, multi-faculty lab pools, and reserved Association blocks.",
    "Enterprise-Grade Full Stack Platform: Delivered a complete, decoupled web application combining FastAPI backend, SQLAlchemy ORM, and React 18 / Tailwind CSS frontend.",
    "Academic Transparency: Built with automated verification testing, instant CSV export, and print-ready PDF reporting meeting Anna University / CIT standards."
]

for c in concls:
    pr = tf_s.add_paragraph()
    pr.text = "✔  " + c
    pr.font.size = Pt(12.5)
    pr.font.color.rgb = TEXT_DARK
    pr.space_before = Pt(14)

# ==================== SLIDE 14: THANK YOU ====================
slide14 = prs.slides.add_slide(blank_layout)
bg14 = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg14.fill.solid()
bg14.fill.fore_color.rgb = BG_DARK
bg14.line.fill.background()

tb14 = slide14.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.33), Inches(3.5))
tf14 = tb14.text_frame
tf14.word_wrap = True

p = tf14.paragraphs[0]
p.text = "THANK YOU!"
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = TEXT_LIGHT
p.alignment = PP_ALIGN.CENTER

p2 = tf14.add_paragraph()
p2.text = "Questions & Technical Demonstration"
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = RGBColor(129, 140, 248) # Indigo 400
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(12)

p3 = tf14.add_paragraph()
p3.text = "SOWNDARIYA R (2303717610422123)  |  PRAVEENKUMAR B (2303717610421108)\nDepartment of Computer Science and Engineering\nCoimbatore Institute of Technology"
p3.font.size = Pt(13)
p3.font.color.rgb = RGBColor(203, 213, 225) # Slate 300
p3.alignment = PP_ALIGN.CENTER
p3.space_before = Pt(20)

output_pptx = r"s:\Time Table Generator\PROJECT_PRESENTATION.pptx"
prs.save(output_pptx)
print(f"Successfully generated PowerPoint presentation at: {output_pptx}")
