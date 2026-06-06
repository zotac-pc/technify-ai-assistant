# Week 1 Task Instructions — AI Team 1
## Technify Academic AI Assistant (TAIA)

**Period:** June 7 - June 13, 2026  
**Goal:** Project setup, environment configuration, architecture design, and research  
**Daily Standup:** [Set your meeting time] — Every member shares: What I did, What I'll do, Any blockers  

---

## EVERYONE — Day 1 Tasks (June 7)

Complete these tasks TODAY:

### Task 1.1: Read the Project Document (MANDATORY)
- **File:** `docs/PROJECT_DOCUMENT.md`
- Read the ENTIRE document carefully
- Understand what we're building, the architecture, and your role
- Write down any questions you have for the team meeting

### Task 1.2: Setup Development Environment
```
Step 1: Install Python 3.10+ (if not installed)
        Download from: https://www.python.org/downloads/
        IMPORTANT: Check "Add Python to PATH" during installation

Step 2: Install Git (if not installed)
        Download from: https://git-scm.com/downloads

Step 3: Install VS Code (if not installed)
        Download from: https://code.visualstudio.com/

Step 4: Install VS Code Extensions:
        - Python (by Microsoft)
        - Pylance (by Microsoft)
        - GitLens
        - REST Client (for testing APIs)
```

### Task 1.3: Clone Repository & Setup
```bash
# Clone the repo (Team Lead will share the URL)
git clone <REPO_URL>
cd technify-ai-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Test the server
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs in browser
# You should see the Swagger API documentation page
```

### Task 1.4: Verify Data Generation
```bash
# Generate synthetic test data
python scripts/generate_data.py

# Check that 5 JSON files were created in data/synthetic/
# - students.json (1,000 records)
# - faculty.json (100 records)
# - courses.json (100 records)
# - attendance.json (10,000 records)
# - exams.json (5,000 records)
```

### Task 1.5: Learn Git Basics
If you're new to Git, learn these commands:
```bash
git status              # See what files changed
git add .               # Stage all changes
git commit -m "message" # Commit with a message
git push                # Push to GitHub
git pull                # Get latest changes
git checkout -b name    # Create a new branch
```

**Rule:** NEVER push directly to `main` branch. Always create a feature branch.

---

## ROLE-SPECIFIC TASKS (June 8 - June 13)

---

### Member A — Backend Developer 1 (Auth & API Gateway)

**Week 1 Focus:** Learn FastAPI + JWT Authentication

#### Task A1: FastAPI Tutorial (June 8)
- Watch: "FastAPI Full Course" on YouTube (any ~1hr tutorial)
- Practice: Create a simple FastAPI app with 3 endpoints
- Read: https://fastapi.tiangolo.com/tutorial/

#### Task A2: JWT Research (June 9)
- Understand what JWT tokens are and how they work
- Read: https://jwt.io/introduction
- Study the `python-jose` library: https://github.com/mpdavis/python-jose
- Write a small script that creates and validates a JWT token

#### Task A3: Design Auth Middleware (June 10-11)
- Plan how JWT validation will work in our FastAPI app
- Design the middleware that intercepts every request and validates the token
- Write pseudocode for the authentication flow
- Share your design with the Team Lead for review

#### Task A4: Start Building Auth Module (June 12-13)
- Create `app/auth/jwt_handler.py` with basic JWT validation
- Create `app/auth/rbac.py` with role checking logic
- Write basic tests in `tests/test_auth.py`

**Deliverable by June 13:** JWT validation working with test tokens

---

### Member B — Backend Developer 2 (ERP Connector & Audit)

**Week 1 Focus:** Learn API integration + Build Mock ERP

#### Task B1: API Integration Research (June 8)
- Learn the `httpx` library (async HTTP client)
- Read: https://www.python-httpx.org/
- Practice: Write a script that calls a public API and parses JSON response

#### Task B2: Study Synthetic Data Structure (June 9)
- Open each JSON file in `data/synthetic/`
- Understand the data format for students, faculty, courses, attendance, exams
- Document the data fields (create a data dictionary)

#### Task B3: Design Mock ERP API (June 10-11)
- Design REST API endpoints that the mock ERP will serve
- Plan URL structure, request/response formats
- Example endpoints:
  ```
  GET /api/v1/student/{student_id}
  GET /api/v1/student/{student_id}/attendance
  GET /api/v1/student/{student_id}/results
  GET /api/v1/student/{student_id}/courses
  GET /api/v1/faculty/{faculty_id}/courses
  GET /api/v1/admin/statistics
  ```
- Share API design with Team Lead

#### Task B4: Build Mock ERP Server (June 12-13)
- Create `mock_erp/main.py` — FastAPI app that serves test data
- Create `mock_erp/routes.py` — All mock endpoints
- The mock ERP should read from `data/synthetic/*.json` and return data
- Run on port 8001 so it doesn't conflict with our main app (port 8000)

**Deliverable by June 13:** Mock ERP running at http://localhost:8001/docs with at least 5 working endpoints

---

### Member C — AI/NLP Developer (LangChain & Prompts)

**Week 1 Focus:** Learn LangChain fundamentals

#### Task C1: LangChain Tutorial (June 8)
- Watch: "LangChain Full Tutorial" on YouTube
- Read: https://python.langchain.com/docs/get_started/introduction
- Understand concepts: Chains, Agents, Tools, Memory, Prompts

#### Task C2: OpenAI API Practice (June 9)
- Get familiar with the OpenAI API
- Write a simple Python script that sends a question to GPT and gets a response
- Understand tokens, temperature, system prompts, user prompts

#### Task C3: LangChain Hands-on Practice (June 10-11)
- Build a simple chatbot using LangChain + OpenAI
- Practice with:
  - PromptTemplate
  - ChatOpenAI
  - ConversationBufferMemory
  - LLMChain
- Build a conversation that remembers context (Module 5 preview)

#### Task C4: Design Prompt Templates (June 12-13)
- Design prompt templates for:
  - Attendance queries
  - Result/GPA queries
  - Course queries
  - General academic questions
- Use LangChain's PromptTemplate format
- Share prompts with Team Lead for review

**Deliverable by June 13:** Basic chatbot using LangChain that can hold a multi-turn conversation

---

### Member D — Knowledge Base / RAG Developer

**Week 1 Focus:** Learn RAG (Retrieval Augmented Generation) + ChromaDB

#### Task D1: RAG Concept Research (June 8)
- Watch: "RAG Explained" videos on YouTube
- Understand: Embeddings, Vector Databases, Similarity Search
- Read: https://docs.trychroma.com/getting-started

#### Task D2: ChromaDB Tutorial (June 9)
- Install ChromaDB and run basic examples
- Practice: Create a collection, add documents, query for similar documents
- Understand: Embedding functions, distance metrics

#### Task D3: Create Sample University Documents (June 10-11)
- Create 5-8 text/markdown files with realistic university policies:
  - `attendance_policy.md` — Minimum 75% attendance required, etc.
  - `exam_rules.md` — Exam conduct rules, allowed materials, etc.
  - `grading_policy.md` — Grade boundaries (A+, A, B, etc.)
  - `degree_requirements.md` — Credit hours needed for graduation
  - `fee_policy.md` — Payment deadlines, late fees, scholarships
  - `academic_calendar.md` — Semester dates, holidays
  - `student_conduct.md` — Code of conduct, disciplinary procedures
- Store in `data/documents/`

#### Task D4: Build Document Ingestion Pipeline (June 12-13)
- Write a script that:
  1. Reads all documents from `data/documents/`
  2. Splits them into chunks
  3. Creates embeddings
  4. Stores in ChromaDB
- Test: Query "What is the attendance policy?" and get relevant chunks

**Deliverable by June 13:** ChromaDB loaded with university documents, able to answer basic policy queries

---

### Member E — Data Engineer + QA Tester

**Week 1 Focus:** Data quality + Testing setup + Documentation

#### Task E1: Validate Synthetic Data (June 8)
- Run `python scripts/generate_data.py`
- Check all 5 JSON files for correctness
- Verify:
  - Are student IDs unique?
  - Are faculty IDs linked correctly to courses?
  - Are attendance percentages realistic?
  - Are exam grades calculated correctly?
- Report any issues

#### Task E2: Enhance Data Generator (June 9-10)
- Add more realistic data if needed:
  - Fee payment records with dates
  - Timetable data (weekly schedule per course)
  - Assignment data (title, due date, submission status)
- Improve the data generator script

#### Task E3: Setup Testing Framework (June 11)
- Configure `pytest` for the project
- Create `tests/conftest.py` with common test fixtures
- Write 5 basic tests:
  - Test server starts correctly
  - Test health endpoint returns 200
  - Test /docs endpoint loads
  - Test invalid JWT is rejected
  - Test synthetic data files exist and have correct record counts

#### Task E4: Create Data Dictionary Document (June 12-13)
- Create `docs/data_dictionary.md` with:
  - All data fields for each entity (Student, Faculty, Course, etc.)
  - Data types
  - Valid values / constraints
  - Example records
  - Relationships between entities

**Deliverable by June 13:** Enhanced test data, pytest framework running, data dictionary document

---

### Team Lead — Your Tasks

#### Task TL1: Initialize Git Repository (June 7) [DONE]
- [x] Create GitHub/GitLab repository
- [x] Push initial project structure
- [x] Set up branch protection rules on `main`
- [x] Add all team members as collaborators

#### Task TL2: Architecture Diagram (June 8-9)
- Create a professional architecture diagram
- Include: All components, data flow, APIs, security layers
- Tools: draw.io, Excalidraw, or Mermaid diagrams
- Store in `docs/architecture.md`
- This is Deliverable #1!

#### Task TL3: Design API Endpoints (June 10)
- Define all API endpoints our service will expose
- Document request/response formats
- Share with the team and get feedback
- Store in `docs/api_guide.md`

#### Task TL4: Coordinate with Other Teams (June 11-12)
- Meet with the Web/Backend team lead
- Discuss:
  - What ERP APIs we need them to build
  - JWT token format they will use
  - How the chat widget will be embedded in the ERP frontend
- Share a list of required APIs with them

#### Task TL5: Weekly Review (June 13)
- Review all team members' deliverables
- Check if everyone completed their tasks
- Update the project timeline if needed
- Plan Week 2 tasks
- Report progress to CEO

---

## Daily Schedule Template

| Time | Activity |
|------|----------|
| 09:00 - 09:15 | Daily standup meeting |
| 09:15 - 12:30 | Development work |
| 12:30 - 13:30 | Lunch break |
| 13:30 - 16:30 | Development work |
| 16:30 - 17:00 | Push code, update progress |

---

## Git Workflow

```
1. NEVER push directly to 'main' branch
2. Create a feature branch for your work:
   git checkout -b feature/jwt-auth
   git checkout -b feature/mock-erp
   git checkout -b feature/langchain-setup
   
3. Commit frequently with clear messages:
   git add .
   git commit -m "Add JWT validation middleware"
   
4. Push your branch:
   git push origin feature/jwt-auth
   
5. Create a Pull Request (PR) on GitHub
6. Team Lead reviews and merges
```

### Branch Naming Convention
```
feature/jwt-auth          (new feature)
feature/mock-erp          (new feature)
bugfix/token-validation   (bug fix)
docs/api-guide            (documentation)
```

---

## Communication

- **Daily Updates:** Post in team group what you completed today
- **Blocked?** Tell the team lead immediately, don't wait
- **Need Help?** Ask in the group, everyone should help each other
- **Code Review:** Submit Pull Requests, don't merge your own code

---

## Week 1 Summary Checklist

By June 13, the following must be DONE:

- [ ] All members: Dev environment set up and running
- [ ] All members: Can run the FastAPI server locally
- [ ] All members: Understand the project (read the project document)
- [ ] Member A: JWT validation module started
- [ ] Member B: Mock ERP server with 5+ endpoints running
- [ ] Member C: Basic LangChain chatbot working
- [ ] Member D: ChromaDB loaded with university documents
- [ ] Member E: Test framework running, data dictionary complete
- [ ] Team Lead: Architecture diagram completed
- [ ] Team Lead: API endpoint design documented
- [ ] Team Lead: Coordination with other teams initiated
- [ ] Git: All members have pushed at least one commit

---

*Good luck team! Let's build something amazing this week!*
