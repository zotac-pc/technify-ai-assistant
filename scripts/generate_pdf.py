"""Generate Team PDF Document for Technify AI Assistant Project"""
from fpdf import FPDF
import os

GITHUB = "https://github.com/zotac-pc/technify-ai-assistant"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "TAIA_Team_Document.pdf")

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Technify Academic AI Assistant (TAIA) - AI Team 1", align="C")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, t):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 90, 180)
        self.cell(0, 12, t, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 90, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)
        self.set_x(10)

    def sub_title(self, t):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, t, new_x="LMARGIN", new_y="NEXT")

    def body(self, t):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, t)
        self.ln(2)

    def bullet(self, t):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(10)
        self.multi_cell(190, 5.5, "   - " + t)

    def table_row(self, cols, widths, bold=False):
        self.set_font("Helvetica", "B" if bold else "", 9)
        h = 7
        for i, c in enumerate(cols):
            self.cell(widths[i], h, str(c), border=1, align="C" if bold else "L")
        self.ln(h)


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ============================================================
# COVER PAGE
# ============================================================
pdf.add_page()
pdf.ln(40)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(0, 70, 160)
pdf.cell(0, 15, "Technify Academic AI Assistant", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 12, "(TAIA)", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_draw_color(0, 90, 180)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(10)
pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(60, 60, 60)
pdf.cell(0, 8, "AI Team 1 - Project Document", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "Technify Software House", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font("Helvetica", "", 11)
pdf.cell(0, 8, "Duration: June 7, 2026 - July 31, 2026 (8 Weeks)", align="C", new_x="LMARGIN", new_y="NEXT")
# FIXED: 8 Members
pdf.cell(0, 8, "Team Size: 8 Members", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(15)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(0, 90, 180)
pdf.cell(0, 8, f"GitHub: {GITHUB}", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(30)
pdf.set_font("Helvetica", "I", 10)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 8, "CONFIDENTIAL - For AI Team 1 Members Only", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "Document Version 1.0 | June 7, 2026", align="C", new_x="LMARGIN", new_y="NEXT")

# ============================================================
# TABLE OF CONTENTS
# ============================================================
pdf.add_page()
pdf.section_title("Table of Contents")
toc = [
    "1. Project Overview",
    "2. What We Are Building",
    "3. How It Works - System Flow",
    "4. System Architecture",
    "5. Technology Stack",
    "6. The 5 Modules",
    "7. Features By User Role",
    "8. Security & Privacy",
    "9. Project Folder Structure",
    "10. GitHub Repository Setup",
    "11. Deliverables & Success Criteria",
    "12. Team Roles & Assignments",
    "13. 8-Week Timeline",
    "14. Week 1 Tasks (Detailed)",
    "15. Setup Instructions",
]
for item in toc:
    pdf.bullet(item)

# ============================================================
# 1. PROJECT OVERVIEW
# ============================================================
pdf.add_page()
pdf.section_title("1. Project Overview")
pdf.body("Technify is building a University ERP (Enterprise Resource Planning) system - a complete university management software. Multiple intern teams are working on different parts:")
w = [35, 45, 110]
pdf.table_row(["Team", "Technology", "Responsibility"], w, bold=True)
pdf.table_row(["Web App", "React + Next.js", "ERP web frontend"], w)
pdf.table_row(["Backend", "Laravel + PostgreSQL", "ERP backend & database"], w)
pdf.table_row(["Mobile", "Flutter", "ERP mobile app"], w)
pdf.table_row(["AI Team (Us)", "Python + FastAPI", "AI-powered academic assistant"], w)
pdf.table_row(["Data Science", "Python", "Analytics & dashboards"], w)
pdf.ln(5)
pdf.body("OUR SCOPE: We build ONLY the AI Assistant microservice. We do NOT build the ERP itself. Our AI service is a separate application that communicates with the ERP through REST APIs.")
pdf.ln(3)
pdf.sub_title("The Golden Rule")
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(180, 0, 0)
pdf.multi_cell(0, 6, "The AI Assistant is NOT allowed to access the database directly. All data access must occur through secure ERP APIs.")
pdf.ln(5)

# ============================================================
# 2. WHAT WE ARE BUILDING
# ============================================================
pdf.set_text_color(30, 30, 30)
pdf.section_title("2. What We Are Building")
pdf.body("We are building a smart AI chatbot that sits inside the university ERP system. When a user (student, teacher, or admin) opens the ERP, they can talk to the AI assistant in natural language.")
pdf.sub_title("Example Conversations")
pdf.set_font("Courier", "", 9)
pdf.multi_cell(0, 5, 'Student: "What is my attendance in Web Engineering?"\nAI: "Your attendance in Web Engineering (CS-301) is 78%.\n     You have attended 25 out of 32 classes."')
pdf.ln(3)
pdf.multi_cell(0, 5, 'Faculty: "Which students have low attendance?"\nAI: "8 students have attendance below 75% in Database Systems..."')
pdf.ln(3)
pdf.multi_cell(0, 5, 'Admin: "What is the fee collection status?"\nAI: "Total Expected: PKR 425M | Collected: PKR 382.5M (90%)"')
pdf.ln(5)

# ============================================================
# 3. HOW IT WORKS
# ============================================================
pdf.add_page()
pdf.section_title("3. How It Works - System Flow")
steps = [
    "Step 1: User logs into ERP (web or mobile app)",
    "Step 2: ERP authenticates the user and creates a JWT token",
    "Step 3: User opens the AI Assistant (chatbot widget in the ERP)",
    "Step 4: ERP sends UserID + Role + JWT Token to our AI service",
    "Step 5: Our AI validates the JWT token (checks signature & expiry)",
    "Step 6: AI understands the question using LLM (GPT or Llama)",
    "Step 7: AI calls the appropriate ERP API to fetch data",
    "         Example: GET /api/v1/student/STU-0042/attendance",
    "Step 8: ERP returns ONLY the data this user is allowed to see",
    "Step 9: AI formats a human-readable response using the LLM",
    "Step 10: User sees the answer in the chat window",
]
for s in steps:
    pdf.bullet(s)
pdf.ln(5)

# ============================================================
# 4. ARCHITECTURE
# ============================================================
pdf.section_title("4. System Architecture")
pdf.body("Our system follows a microservice architecture. The AI assistant is completely separate from the ERP. The ERP team builds the frontend (React), backend (Laravel), and database (PostgreSQL). We build the AI service (FastAPI + LangChain + ChromaDB).")
pdf.body("Key components of our AI microservice:")
components = [
    ["FastAPI Gateway", "Receives requests, validates JWT, routes to AI engine"],
    ["LangChain Engine", "Processes questions, determines intent, calls tools"],
    ["ERP Connector", "HTTP client that calls ERP backend APIs"],
    ["ChromaDB (RAG)", "Vector database storing university policy documents"],
    ["LLM (GPT/Llama)", "The AI brain that generates natural language responses"],
    ["Audit Logger", "Logs every request for security compliance"],
]
w2 = [45, 145]
pdf.table_row(["Component", "Purpose"], w2, bold=True)
for c in components:
    pdf.table_row(c, w2)
pdf.ln(3)
pdf.body("Why separate microservice? (1) Independent development - we use Python, ERP uses PHP. (2) Independent deployment. (3) Reusability in other Technify products. (4) Independent scaling.")

# ============================================================
# 5. TECH STACK
# ============================================================
pdf.add_page()
pdf.section_title("5. Technology Stack")
w3 = [40, 30, 120]
pdf.table_row(["Technology", "Version", "Purpose"], w3, bold=True)
stack = [
    ["Python", "3.10+", "Core programming language"],
    ["FastAPI", "0.115+", "Web framework - our API server"],
    ["LangChain", "0.3+", "AI/LLM framework - prompts, RAG, tools"],
    ["ChromaDB", "1.0+", "Vector database for document search"],
    ["OpenAI GPT", "Phase 1", "LLM brain (switch to Llama in Phase 2)"],
    ["JWT", "3.4+", "Authentication token validation"],
    ["httpx", "0.28+", "HTTP client for calling ERP APIs"],
    ["Faker", "37+", "Synthetic test data generation"],
    ["pytest", "8.0+", "Automated testing framework"],
]
for s in stack:
    pdf.table_row(s, w3)
pdf.ln(5)

# ============================================================
# 6. THE 5 MODULES
# ============================================================
pdf.section_title("6. The 5 Modules We Must Build")
modules = [
    ("Module 1: User Authentication", "Validate JWT tokens from ERP, check user role and permissions before answering any question. Reject expired or fake tokens."),
    ("Module 2: Academic Info Retrieval", "Call ERP APIs to fetch attendance, results, GPA, timetable, assignments, fee records. Format data for the LLM."),
    ("Module 3: Knowledge Base (RAG)", "Store university policy documents in ChromaDB. When users ask policy questions, retrieve relevant document chunks and generate accurate answers."),
    ("Module 4: Study Recommendations", "Generate personalized study schedules, recommend courses, suggest learning resources based on student academic data."),
    ("Module 5: Conversation Management", "Maintain context across multiple messages. Follow-up questions like 'What about Web Engineering?' should work correctly."),
]
for title, desc in modules:
    pdf.sub_title(title)
    pdf.body(desc)

# ============================================================
# 7. FEATURES BY ROLE
# ============================================================
pdf.add_page()
pdf.section_title("7. Features By User Role")
pdf.sub_title("Student Features")
for f in [
    "Check attendance (overall and per course)",
    "View pending assignments",
    "Check exam schedule",
    "View GPA and results",
    "Check fee status",
    "View registered courses and timetable",
    "Generate study plans",
    "Ask about university policies",
]:
    pdf.bullet(f)
pdf.ln(3)
pdf.sub_title("Faculty Features")
for f in ["View students with low attendance", "Check ungraded assignments", "Identify at-risk students", "View course performance statistics"]:
    pdf.bullet(f)
pdf.ln(3)
pdf.sub_title("Admin Features")
for f in ["View total enrollment numbers", "Admission statistics", "Fee collection reports", "Department-wise performance"]:
    pdf.bullet(f)
pdf.ln(5)

# ============================================================
# 8. SECURITY
# ============================================================
pdf.section_title("8. Security & Privacy")
pdf.body("RBAC (Role-Based Access Control): Every request is checked against the user's role. Students see only their own data. Faculty see only their assigned courses. Admins see aggregated statistics.")
pdf.sub_title("The AI Must NEVER:")
for f in ["Modify marks, attendance, or fees (read-only access)", "Approve admissions", "Access unauthorized data", "Reveal another student's information (0% data leakage)"]:
    pdf.bullet(f)
pdf.ln(3)
pdf.sub_title("Audit Logging")
pdf.body("Every request is logged with: UserID, Role, Query, Response Type, Timestamp, Response Time. Logs are stored for compliance and security review.")

# ============================================================
# 9. PROJECT STRUCTURE
# ============================================================
pdf.add_page()
pdf.section_title("9. Project Folder Structure")
pdf.set_font("Courier", "", 8)
structure = """technify-ai-assistant/
|-- app/                    # Main application code
|   |-- main.py             # FastAPI entry point
|   |-- auth/               # Module 1: JWT & RBAC
|   |-- api/routes/         # API endpoints
|   |-- services/           # Business logic (AI, ERP connector, KB)
|   |-- chains/             # LangChain chains (student, faculty, admin)
|   |-- prompts/            # Prompt templates
|   |-- models/             # Data models
|-- data/
|   |-- synthetic/          # Generated test data (7 JSON files)
|   |-- documents/          # University policy documents (7 files)
|   |-- vector_store/       # ChromaDB storage
|-- docs/                   # All documentation
|-- mock_erp/               # Mock ERP server for testing
|-- scripts/                # Utility scripts
|-- tests/                  # Automated tests
|-- requirements.txt        # Python dependencies
|-- .env.example            # Config template
|-- README.md               # Repository README"""
pdf.multi_cell(0, 4.5, structure)
pdf.ln(5)

# ============================================================
# 10. GITHUB
# ============================================================
pdf.section_title("10. GitHub Repository")
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(0, 90, 180)
pdf.cell(0, 8, GITHUB, new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(30, 30, 30)
pdf.ln(3)
pdf.sub_title("Git Workflow Rules")
for f in [
    "NEVER push directly to 'main' branch",
    "Create feature branches: feature/jwt-auth, feature/mock-erp, etc.",
    "Commit frequently with clear messages",
    "Create Pull Requests for code review",
    "Team Lead reviews and merges PRs",
]:
    pdf.bullet(f)
pdf.ln(5)

# ============================================================
# 11. DELIVERABLES
# ============================================================
pdf.section_title("11. Deliverables & Success Criteria")
w4 = [15, 55, 70, 50]
pdf.table_row(["#", "Deliverable", "Description", "Deadline"], w4, bold=True)
for d in [
    ["1", "Architecture Diagram", "System diagrams & components", "Week 1 (DONE)"],
    ["2", "Prompt Library", "All prompt templates", "Week 2"],
    ["3", "Knowledge Base", "Docs in searchable format", "Week 3"],
    ["4", "Working Prototype", "Web-based chatbot", "Week 5"],
    ["5", "ERP Integration", "API connectors", "Week 5"],
    ["6", "Documentation", "Install, API, User guides", "Week 7"],
]:
    pdf.table_row(d, w4)
pdf.ln(5)
pdf.sub_title("Success Criteria")
w5 = [60, 40, 90]
pdf.table_row(["Criteria", "Target", "How to Test"], w5, bold=True)
for c in [
    ["Response Time", "< 3 seconds", "Measure with timer"],
    ["Accuracy", "90%+", "Test 100 questions"],
    ["Data Leakage", "0%", "Try accessing others data"],
    ["ERP Integration", "Successful", "API calls return correct data"],
    ["Role-Based Security", "Implemented", "Each role sees only their data"],
]:
    pdf.table_row(c, w5)

# ============================================================
# 12. TEAM ROLES - FIXED: 8 Members
# ============================================================
pdf.add_page()
pdf.section_title("12. Team Roles & Assignments")
w6 = [10, 55, 125]
pdf.table_row(["#", "Role", "Responsibilities"], w6, bold=True)
for r in [
    ["1", "Team Lead + AI Architect", "Architecture, LangChain pipeline, code review, coordination"],
    ["2", "Backend Developer 1", "FastAPI endpoints, JWT auth, API gateway, WebSocket"],
    ["3", "Backend Developer 2", "ERP API connectors, data formatting, audit logging, mock ERP"],
    ["4", "AI/NLP Developer", "LangChain chains, prompt engineering, conversation mgmt"],
    ["5", "KB / RAG Developer", "ChromaDB setup, document ingestion, RAG pipeline, chat UI"],
    ["6", "Data Engineer + QA", "Synthetic data, testing, documentation, quality assurance"],
    ["7", "Frontend Developer", "Chat UI, WebSocket integration, role dashboards"],
    ["8", "Security + QA", "Penetration testing, RBAC testing, audit logs, performance"],
]:
    pdf.table_row(r, w6)
pdf.ln(5)

# ============================================================
# 13. TIMELINE
# ============================================================
pdf.section_title("13. 8-Week Timeline")
w7 = [25, 60, 105]
pdf.table_row(["Week", "Phase", "Key Tasks"], w7, bold=True)
for t in [
    ["Week 1", "Setup & Architecture", "Git, venv, architecture diagram, research"],
    ["Week 2", "Foundation", "JWT auth, mock ERP, basic LangChain, prompts"],
    ["Week 3", "Core Features", "Student features, ERP connectors, RAG, memory"],
    ["Week 4", "Advanced Features", "Faculty/admin features, study planner"],
    ["Week 5", "Integration & UI", "Chat UI, WebSocket, full integration"],
    ["Week 6", "Security & Testing", "Penetration testing, accuracy, performance"],
    ["Week 7", "Docs & Polish", "Documentation, open-source LLM, cleanup"],
    ["Week 8", "Final Demo", "Integration with real ERP, demo to CEO"],
]:
    pdf.table_row(t, w7)
pdf.ln(5)

# ============================================================
# 14. WEEK 1 TASKS
# ============================================================
pdf.add_page()
pdf.section_title("14. Week 1 Tasks - Detailed (June 7-13)")
pdf.sub_title("ALL MEMBERS - Day 1 (June 7)")
for d in [
    "Read the complete PROJECT_DOCUMENT.md in the docs/ folder",
    "Install Python 3.10+, Git, VS Code",
    "Clone the GitHub repo: git clone " + GITHUB,
    "Create virtual environment: python -m venv venv",
    "Activate venv: venv\\Scripts\\activate (Windows)",
    "Install dependencies: pip install -r requirements.txt",
    "Copy .env.example to .env",
    "Run server: uvicorn app.main:app --reload",
    "Visit http://localhost:8000/docs to verify Swagger UI loads",
    "Run data generator: python scripts/generate_data.py",
]:
    pdf.bullet(d)

pdf.ln(4)
pdf.sub_title("Member A - Backend Dev 1 (Auth)")
for t in ["Learn FastAPI (YouTube tutorial + docs)", "Study JWT tokens (jwt.io)", "Learn python-jose library", "Design auth middleware (pseudocode)", "Build app/auth/jwt_handler.py", "Build app/auth/rbac.py", "DELIVERABLE: JWT validation working by June 13"]:
    pdf.bullet(t)

pdf.ln(3)
pdf.sub_title("Member B - Backend Dev 2 (ERP Connector)")
for t in ["Learn httpx library (async HTTP client)", "Study synthetic data JSON structure", "Design mock ERP API endpoints", "Build mock_erp/main.py (FastAPI on port 8001)", "Build 5+ mock endpoints serving test data", "DELIVERABLE: Mock ERP running by June 13"]:
    pdf.bullet(t)

pdf.ln(3)
pdf.sub_title("Member C - AI/NLP Developer")
for t in ["Learn LangChain (tutorial + docs)", "Practice OpenAI API calls", "Build basic_chain.py with conversation memory", "Design prompt templates for attendance, results, courses", "DELIVERABLE: Basic LangChain chatbot by June 13"]:
    pdf.bullet(t)

pdf.add_page()
pdf.sub_title("Member D - Knowledge Base / RAG Developer")
for t in ["Learn RAG concepts (YouTube + docs)", "Learn ChromaDB (tutorial + getting started)", "Review 7 policy documents in data/documents/", "Build document ingestion script (split, embed, store)", "Test: Query 'attendance policy' returns relevant chunks", "DELIVERABLE: ChromaDB loaded with docs by June 13"]:
    pdf.bullet(t)

pdf.ln(3)
pdf.sub_title("Member E - Data Engineer + QA")
for t in ["Validate synthetic data (run generate_data.py)", "Check data quality (unique IDs, correct links)", "Timetable and assignment data already included in generator", "Setup pytest framework + conftest.py", "Write 5 basic tests (health endpoint, data files, etc.)", "Create docs/data_dictionary.md", "DELIVERABLE: Enhanced data + test framework by June 13"]:
    pdf.bullet(t)

pdf.ln(3)
pdf.sub_title("Member F - Frontend Developer")
for t in ["Learn WebSocket basics", "Build basic chat UI (HTML/CSS/JS)", "Design 3 role dashboards (Student, Faculty, Admin)", "DELIVERABLE: Basic chat interface by June 13"]:
    pdf.bullet(t)

pdf.ln(3)
pdf.sub_title("Member G - Security + QA")
for t in ["Study OWASP JWT security guidelines", "Create docs/security_checklist.md", "Design RBAC test cases for all 3 roles", "DELIVERABLE: Security checklist ready by June 13"]:
    pdf.bullet(t)

pdf.ln(3)
pdf.sub_title("Team Lead Tasks")
for t in ["Initialize GitHub repo + push code (DONE)", "Create architecture diagram (DONE - docs/architecture.md)", "Design API endpoints (DONE - docs/api_guide.md)", "Coordinate with Web/Backend team leads", "Set up daily standup meetings", "Weekly review meeting on Friday June 13"]:
    pdf.bullet(t)

# ============================================================
# 15. SETUP
# ============================================================
pdf.ln(5)
pdf.section_title("15. Quick Setup Guide")
pdf.set_font("Courier", "", 9)
setup = f"""# Clone the repository
git clone {GITHUB}
cd technify-ai-assistant

# Create and activate virtual environment
python -m venv venv
venv\\Scripts\\activate          # Windows
source venv/bin/activate        # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment config
copy .env.example .env
# Edit .env with your API keys

# Generate test data
python scripts/generate_data.py

# Run the server
uvicorn app.main:app --reload

# Open in browser
# http://localhost:8000/docs"""
pdf.multi_cell(0, 4.5, setup)

# ============================================================
# FINAL PAGE
# ============================================================
pdf.add_page()
pdf.ln(30)
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(0, 70, 160)
pdf.cell(0, 15, "Let's Build Something Amazing!", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(60, 60, 60)
pdf.cell(0, 8, "AI Team 1 - Technify Software House", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "June - July 2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(15)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(0, 90, 180)
pdf.cell(0, 8, f"GitHub: {GITHUB}", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)
pdf.set_font("Helvetica", "I", 10)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 8, "This document is confidential.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "For AI Team 1 members only.", align="C", new_x="LMARGIN", new_y="NEXT")

# SAVE
os.makedirs(os.path.dirname(OUT), exist_ok=True)
pdf.output(OUT)
print(f"PDF generated: {os.path.abspath(OUT)}")