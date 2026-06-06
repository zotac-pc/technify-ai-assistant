# Technify Academic AI Assistant (TAIA)
## Complete Project Document — AI Team 1

---

**Document Version:** 1.0  
**Date:** June 7, 2026  
**Team:** AI Team 1  
**Team Lead:** [Your Name]  
**Duration:** June 7, 2026 – July 31, 2026 (8 Weeks)  
**Company:** Technify Software House  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [What We Are Building](#2-what-we-are-building)
3. [How It Works](#3-how-it-works)
4. [System Architecture](#4-system-architecture)
5. [Technology Stack](#5-technology-stack)
6. [The 5 Modules](#6-the-5-modules)
7. [Features By User Role](#7-features-by-user-role)
8. [Security & Privacy](#8-security--privacy)
9. [ERP Integration](#9-erp-integration)
10. [Project Structure](#10-project-structure)
11. [Deliverables](#11-deliverables)
12. [Team Roles](#12-team-roles)
13. [8-Week Timeline](#13-8-week-timeline)
14. [Success Criteria](#14-success-criteria)
15. [Out of Scope](#15-out-of-scope)
16. [Setup Instructions](#16-setup-instructions)

---

## 1. Project Overview

Technify is building a **University ERP (Enterprise Resource Planning)** system — a complete university management software. Multiple intern teams are working on different parts of this ERP:

| Team | Technology | What They Build |
|------|-----------|----------------|
| Web App Team | React.js + Next.js | ERP web frontend |
| Backend Team | Laravel + PostgreSQL | ERP backend & database |
| Mobile App Team | Flutter | ERP mobile app |
| **AI Team 1 (Us)** | **Python + FastAPI + LangChain** | **AI-powered academic assistant** |
| Data Science Team | Python | Analytics & dashboards |

### Our Scope

**We build ONLY the AI Assistant microservice.** We do NOT build the ERP itself. Our AI service is a **separate application** that communicates with the ERP through REST APIs.

### The Golden Rule

> **The AI Assistant is NOT allowed to access the database directly.**  
> All data access must occur through secure ERP APIs.

This means we NEVER write SQL queries or touch PostgreSQL. Instead, we call the ERP's API endpoints (built by the Laravel team) to fetch data.

---

## 2. What We Are Building

We are building a **smart AI chatbot** that sits inside the university ERP system. When a user (student, teacher, or admin) opens the ERP, they can talk to the AI assistant in natural language.

### Example Conversations

**Student:**
```
Student: What is my attendance?
AI: Your overall attendance is 82%.

Student: What about Web Engineering?
AI: Your attendance in Web Engineering (CS-301) is 78%. 
    You have attended 25 out of 32 classes.
    Note: The minimum required attendance is 75%.

Student: What assignments are pending?
AI: You have 2 pending assignments:
    1. Database Systems - Assignment 3 (Due: June 15)
    2. Web Engineering - Project Proposal (Due: June 18)
```

**Faculty:**
```
Faculty: Which students have low attendance in my Database course?
AI: 8 students have attendance below 75% in Database Systems (CS-201):
    1. Ahmed Khan (STU-0042) - 68%
    2. Fatima Ali (STU-0156) - 71%
    ... [remaining students]

Faculty: Which assignments are ungraded?
AI: You have 3 ungraded assignments:
    1. Database Systems - Assignment 2 (45 submissions, 0 graded)
    2. Database Systems - Quiz 3 (42 submissions, 0 graded)
    3. Database Lab - Lab Report 5 (38 submissions, 12 graded)
```

**Admin:**
```
Admin: How many students are enrolled this semester?
AI: Total enrollment for Spring 2026: 4,250 students
    - Computer Science: 850
    - Information Technology: 720
    - Software Engineering: 680
    ...

Admin: What is the fee collection status?
AI: Fee Collection Summary (Spring 2026):
    - Total Expected: PKR 425,000,000
    - Collected: PKR 382,500,000 (90%)
    - Pending: PKR 42,500,000 (10%)
```

---

## 3. How It Works

### Step-by-Step Flow

```
Step 1: User logs into ERP (web or mobile)
Step 2: ERP authenticates the user and creates a JWT token
Step 3: User opens the AI Assistant (chatbot widget)
Step 4: ERP sends user's info to our AI service:
        - UserID (e.g., "STU-0042")
        - Role (e.g., "student")
        - JWT Token (encrypted proof of identity)
Step 5: Our AI validates the JWT token (checks if it's real and not expired)
Step 6: AI understands the question using LLM (GPT/Llama)
Step 7: AI calls the appropriate ERP API to get data
        Example: GET /api/v1/student/attendance?student_id=STU-0042
Step 8: ERP returns ONLY the data this user is allowed to see
Step 9: AI formats a human-readable response
Step 10: User sees the answer in the chat window
```

### Visual Flow

```
                    +------------------+
                    |      User        |
                    | (Student/Faculty |
                    |    /Admin)       |
                    +--------+---------+
                             |
                    Logs into ERP
                             |
                    +--------v---------+
                    |  ERP Frontend    |
                    | (React + Next.js)|
                    +--------+---------+
                             |
                    Opens AI Chat
                             |
                    +--------v---------+
                    | ERP Backend      |
                    | (Laravel)        |
                    | Sends: UserID,   |
                    | Role, JWT Token  |
                    +--------+---------+
                             |
                    API Call (REST)
                             |
            +----------------v-----------------+
            |    OUR AI SERVICE (FastAPI)       |
            |                                  |
            |  1. Validate JWT Token           |
            |  2. Check Role Permissions       |
            |  3. Understand Question (LLM)    |
            |  4. Call ERP APIs for Data        |
            |  5. Format Response              |
            |  6. Log the Request (Audit)      |
            |                                  |
            +---+------------+-------------+---+
                |            |             |
         +------v---+ +-----v------+ +----v-------+
         | LangChain| | ChromaDB   | | ERP APIs   |
         | + LLM    | | (Knowledge | | (Data      |
         | (GPT /   | |  Base)     | |  Retrieval)|
         | Llama)   | +------------+ +------------+
         +----------+
```

---

## 4. System Architecture

Our system follows a **microservice architecture**. The AI assistant is completely separate from the ERP:

```
+-----------------------------------------------------------+
|                     TECHNIFY ERP SYSTEM                     |
|                                                             |
|  +------------------+    +------------------+               |
|  | React Frontend   |    | Flutter Mobile   |               |
|  | (Next.js)        |    | App              |               |
|  +--------+---------+    +--------+---------+               |
|           |                       |                         |
|           +----------++-----------+                         |
|                      ||                                     |
|              +-------vv--------+                            |
|              | Laravel Backend |                            |
|              | (REST APIs)     |                            |
|              +-------+---------+                            |
|                      |                                      |
|              +-------v---------+                            |
|              | PostgreSQL      |                            |
|              | Database        |                            |
|              +-----------------+                            |
+-----------------------------------------------------------+
                       |
                 REST API Calls
                       |
+-----------------------------------------------------------+
|              OUR AI MICROSERVICE                            |
|                                                             |
|  +------------------+    +------------------+               |
|  | FastAPI Server   |    | LangChain        |               |
|  | (API Gateway)    +--->| (AI Engine)      |               |
|  +------------------+    +--------+---------+               |
|                                   |                         |
|                          +--------v---------+               |
|                          | LLM (GPT/Llama) |               |
|                          +------------------+               |
|                                                             |
|  +------------------+    +------------------+               |
|  | ChromaDB         |    | Audit Logger     |               |
|  | (Vector Store)   |    | (Request Logs)   |               |
|  +------------------+    +------------------+               |
+-----------------------------------------------------------+
```

### Why Separate Microservice?

1. **Independent Development:** We work in Python, ERP team works in PHP/Laravel. No conflicts.
2. **Independent Deployment:** We can update the AI without touching the ERP.
3. **Reusability:** This AI service can later be used in other Technify products.
4. **Scalability:** AI service can be scaled independently based on load.

---

## 5. Technology Stack

### What We Use

| Technology | Version | Purpose | Why This? |
|-----------|---------|---------|-----------|
| **Python** | 3.10+ | Core programming language | Best ecosystem for AI/ML |
| **FastAPI** | 0.115+ | Web framework (our API server) | Fast, modern, auto-generates docs |
| **LangChain** | 0.3+ | AI/LLM framework | Prompt management, RAG, tool calling |
| **ChromaDB** | 1.0+ | Vector database | Store university documents for search |
| **OpenAI GPT** | GPT-4o-mini | LLM (Phase 1) | Easiest to start with |
| **Llama/Mistral** | Latest | LLM (Phase 2) | Open-source, free, private |
| **JWT (python-jose)** | 3.4+ | Authentication | Validate ERP tokens |
| **httpx** | 0.28+ | HTTP client | Call ERP APIs asynchronously |
| **Faker** | 37+ | Test data generator | Generate realistic test data |
| **pytest** | 8.4+ | Testing framework | Automated tests |

### What We DON'T Use

| Technology | Why Not |
|-----------|---------|
| Laravel/PHP | That's the ERP team's job |
| PostgreSQL | We don't access the database directly |
| React/Next.js | The ERP frontend team handles the UI |
| Flutter | The mobile team handles the app |

---

## 6. The 5 Modules

### Module 1: User Authentication & Verification

**Purpose:** Verify that the user is who they claim to be.

**How it works:**
- Receives JWT token from ERP
- Validates the token signature and expiry
- Extracts UserID and Role from the token
- Checks permissions before answering any question

**Files:**
- `app/auth/jwt_handler.py` — JWT validation logic
- `app/auth/rbac.py` — Role-Based Access Control

---

### Module 2: Academic Information Retrieval

**Purpose:** Fetch academic data from the ERP via APIs.

**Data we can retrieve:**
- Attendance records
- Exam results / GPA
- Course registrations
- Timetable / Schedule
- Assignment status
- Fee records

**How it works:**
- AI determines what data is needed based on the question
- Calls the appropriate ERP API endpoint
- Parses the JSON response
- Returns formatted data to the LLM for response generation

**Example API calls:**
```
GET /api/v1/student/{id}/attendance
GET /api/v1/student/{id}/results
GET /api/v1/student/{id}/timetable
GET /api/v1/student/{id}/assignments
GET /api/v1/student/{id}/fees
GET /api/v1/faculty/{id}/courses
GET /api/v1/faculty/{id}/students
GET /api/v1/admin/statistics
```

**Files:**
- `app/services/erp_connector.py` — All ERP API calls
- `app/chains/student_chain.py` — Student-specific logic
- `app/chains/faculty_chain.py` — Faculty-specific logic
- `app/chains/admin_chain.py` — Admin-specific logic

---

### Module 3: Knowledge Base (RAG)

**Purpose:** Answer questions about university policies using uploaded documents.

**What is RAG?**
RAG = Retrieval Augmented Generation. Instead of the LLM guessing answers about university policies, we:
1. Upload policy documents (PDFs, text files) into ChromaDB
2. Convert them into searchable vector embeddings
3. When a user asks a policy question, we find the relevant document chunks
4. Send those chunks to the LLM along with the question
5. The LLM generates an accurate answer based on actual documents

**Documents to include:**
- Attendance policy
- Examination rules
- Grading policy
- Degree requirements
- Fee structure
- Academic calendar
- Student code of conduct
- Faculty handbook

**Files:**
- `app/services/knowledge_base.py` — ChromaDB operations
- `data/documents/` — PDF/text source files
- `data/vector_store/` — ChromaDB storage

---

### Module 4: Study Recommendations

**Purpose:** Help students with academic planning.

**Features:**
- Generate personalized study schedules based on exam dates
- Recommend courses based on student's department and semester
- Suggest learning resources
- Identify weak subjects based on grades

**Files:**
- `app/services/study_planner.py` — Recommendation logic
- `app/prompts/study.py` — Study-related prompts

---

### Module 5: Conversation Management

**Purpose:** Maintain context across multiple messages in a conversation.

**Example:**
```
Student: What is my attendance?
AI: Your overall attendance is 82%.

Student: What about Web Engineering?
AI: Your attendance in Web Engineering is 78%.
    (The AI understood "what about" refers to attendance)

Student: Is that enough to sit in the exam?
AI: The minimum attendance requirement is 75%. 
    Your 78% in Web Engineering meets the threshold.
    You are eligible to sit in the exam.
```

**How it works:**
- Each conversation has a unique session ID
- Previous messages are stored in memory
- Context is sent to the LLM with each new question
- Session expires after inactivity

**Files:**
- `app/services/ai_service.py` — Conversation orchestration
- Uses LangChain's ConversationBufferMemory

---

## 7. Features By User Role

### Student Features

| # | Feature | Question Example | ERP API Used |
|---|---------|-----------------|--------------|
| 1 | Attendance Check | "What is my attendance?" | `/student/{id}/attendance` |
| 2 | Pending Assignments | "What assignments are pending?" | `/student/{id}/assignments` |
| 3 | Exam Schedule | "When is my next exam?" | `/student/{id}/exams` |
| 4 | GPA/Results | "What is my GPA?" | `/student/{id}/results` |
| 5 | Fee Status | "Show my fee status" | `/student/{id}/fees` |
| 6 | Registered Courses | "Show my courses" | `/student/{id}/courses` |
| 7 | Timetable | "Show my timetable" | `/student/{id}/timetable` |
| 8 | Study Plan | "Generate a study plan" | Uses results + exam dates |
| 9 | Policy Questions | "What is the attendance policy?" | Knowledge Base (RAG) |

### Faculty Features

| # | Feature | Question Example | ERP API Used |
|---|---------|-----------------|--------------|
| 1 | Low Attendance Students | "Students with low attendance?" | `/faculty/{id}/course/{id}/attendance` |
| 2 | Ungraded Assignments | "Which assignments need grading?" | `/faculty/{id}/assignments` |
| 3 | At-Risk Students | "Students at risk of failure?" | `/faculty/{id}/course/{id}/students` |
| 4 | Course Statistics | "Show course performance stats" | `/faculty/{id}/course/{id}/stats` |

### Admin Features

| # | Feature | Question Example | ERP API Used |
|---|---------|-----------------|--------------|
| 1 | Total Students | "How many students are enrolled?" | `/admin/statistics/students` |
| 2 | Admission Stats | "Show admission statistics" | `/admin/statistics/admissions` |
| 3 | Fee Collection | "Fee collection status?" | `/admin/statistics/fees` |
| 4 | Department Performance | "Department-wise performance?" | `/admin/statistics/departments` |

---

## 8. Security & Privacy

### Role-Based Access Control (RBAC)

Every request is checked against the user's role:

| Role | Can Access | Cannot Access |
|------|-----------|--------------|
| Student | Own profile, attendance, results, fees | Other students' data |
| Faculty | Their assigned courses & students | Other faculty's courses |
| Admin | University-wide statistics | Individual student records (unless authorized) |
| Finance | Fee-related data | Academic records |
| Exam Officer | Exam-related data | Fee records |

### Privacy Rules

- **Student A CANNOT see Student B's data** — Zero tolerance
- Faculty can ONLY see students in their assigned courses
- Admin sees aggregated statistics, not individual records
- All data flows through ERP APIs which enforce their own permissions

### What the AI Must NEVER Do

| Forbidden Action | Why |
|-----------------|-----|
| Modify marks | Read-only access |
| Modify attendance | Read-only access |
| Modify fees | Read-only access |
| Approve admissions | Not in scope |
| Access unauthorized data | Security violation |
| Reveal another student's info | Privacy violation |

### Audit Logging

Every single request to the AI must be logged:

```json
{
    "log_id": "LOG-000001",
    "user_id": "STU-0042",
    "role": "student",
    "query": "What is my attendance?",
    "response_type": "attendance_query",
    "timestamp": "2026-06-07T10:30:00Z",
    "ip_address": "192.168.1.100",
    "response_time_ms": 1200
}
```

---

## 9. ERP Integration

### How We Communicate with ERP

```
Our AI Service  ----REST API (JSON)---->  ERP Backend (Laravel)
                <---JSON Response------
```

### Authentication Flow

```
1. User logs into ERP
2. ERP issues JWT Token:
   {
     "user_id": "STU-0042",
     "role": "student",
     "department": "Computer Science",
     "exp": 1719345600  (expiry timestamp)
   }
3. User opens AI chat widget
4. ERP frontend sends to our API:
   POST /api/v1/chat
   Headers: { "Authorization": "Bearer <JWT_TOKEN>" }
   Body: { "message": "What is my attendance?" }
5. Our AI validates the JWT
6. Our AI calls ERP API with the same JWT:
   GET /api/v1/student/STU-0042/attendance
   Headers: { "Authorization": "Bearer <JWT_TOKEN>" }
7. ERP returns data (only what STU-0042 is allowed to see)
8. AI generates response
```

### Mock APIs

Since the ERP won't be ready immediately, we build **mock APIs** — fake endpoints that return test data. This way we can develop and test without waiting for the Laravel team.

When the real ERP APIs are ready, we simply change the base URL in our config.

---

## 10. Project Structure

```
technify-ai-assistant/
|
|-- app/                         # Main application code
|   |-- __init__.py
|   |-- main.py                  # FastAPI entry point
|   |-- config.py                # Settings & environment variables
|   |
|   |-- auth/                    # Module 1: Authentication
|   |   |-- __init__.py
|   |   |-- jwt_handler.py       # JWT validation
|   |   |-- rbac.py              # Role-based access control
|   |
|   |-- api/                     # API routes
|   |   |-- __init__.py
|   |   |-- routes/
|   |   |   |-- chat.py          # POST /api/v1/chat
|   |   |   |-- health.py        # GET /health
|   |   |   |-- admin.py         # Admin endpoints
|   |   |-- middleware/
|   |       |-- audit_log.py     # Request logging
|   |
|   |-- services/                # Business logic
|   |   |-- __init__.py
|   |   |-- ai_service.py        # LangChain orchestration
|   |   |-- erp_connector.py     # ERP API calls
|   |   |-- knowledge_base.py    # ChromaDB / RAG
|   |   |-- study_planner.py     # Study recommendations
|   |
|   |-- chains/                  # LangChain chains
|   |   |-- __init__.py
|   |   |-- student_chain.py     # Student question handling
|   |   |-- faculty_chain.py     # Faculty question handling
|   |   |-- admin_chain.py       # Admin question handling
|   |
|   |-- prompts/                 # Prompt templates
|   |   |-- __init__.py
|   |   |-- attendance.py        # Attendance query prompts
|   |   |-- results.py           # Result query prompts
|   |   |-- policy.py            # Policy query prompts
|   |
|   |-- models/                  # Data models
|       |-- __init__.py
|       |-- user.py              # User model
|       |-- audit.py             # Audit log model
|
|-- data/
|   |-- synthetic/               # Generated test data (JSON)
|   |-- documents/               # University policy documents
|   |-- vector_store/            # ChromaDB storage
|
|-- mock_erp/                    # Mock ERP for testing
|   |-- __init__.py
|   |-- main.py                  # Mock ERP server
|   |-- routes.py                # Mock API endpoints
|
|-- scripts/
|   |-- generate_data.py         # Synthetic data generator
|
|-- tests/                       # Automated tests
|   |-- __init__.py
|   |-- test_auth.py
|   |-- test_erp_connector.py
|   |-- test_chains.py
|
|-- docs/                        # Documentation
|   |-- PROJECT_DOCUMENT.md      # This document
|   |-- architecture.md          # Architecture details
|   |-- api_guide.md             # API documentation
|   |-- installation.md          # Setup instructions
|   |-- user_guide.md            # End-user guide
|
|-- venv/                        # Python virtual environment (DO NOT COMMIT)
|-- .env                         # Environment variables (DO NOT COMMIT)
|-- .env.example                 # Template for .env
|-- .gitignore                   # Git ignore rules
|-- requirements.txt             # Python dependencies
|-- README.md                    # Repository README
```

---

## 11. Deliverables

We must deliver these 6 items by the end of the internship:

| # | Deliverable | Description | Deadline |
|---|------------|-------------|----------|
| 1 | **Architecture Diagram** | Visual diagram of the system | Week 1 |
| 2 | **Prompt Library** | Collection of all prompt templates | Week 2 |
| 3 | **Knowledge Base** | University documents in searchable format | Week 3 |
| 4 | **Working Prototype** | Web-based chatbot that answers questions | Week 5 |
| 5 | **ERP Integration Layer** | API connectors to the ERP | Week 5 |
| 6 | **Documentation** | Installation, API, Architecture, User guides | Week 7 |

---

## 12. Team Roles

| # | Role | Responsibilities |
|---|------|-----------------|
| 1 | **Team Lead + AI Architect** | Architecture decisions, LangChain pipeline, code review, team coordination, progress reporting |
| 2 | **Backend Developer 1** | FastAPI endpoints, JWT authentication, API gateway, WebSocket for chat |
| 3 | **Backend Developer 2** | ERP API connectors, data formatting, audit logging, mock ERP server |
| 4 | **AI/NLP Developer** | LangChain chains, prompt engineering, conversation management, LLM integration |
| 5 | **Knowledge Base / RAG Developer** | ChromaDB setup, document ingestion, RAG pipeline, chat UI |
| 6 | **Data Engineer + QA Tester** | Synthetic data, testing, documentation, quality assurance |

---

## 13. 8-Week Timeline

### Week 1 (June 7-13): Setup & Architecture
- Project setup (Git, virtual env, dependencies)
- Architecture diagram
- API endpoint design
- Synthetic data generation
- Research (LangChain, FastAPI docs)

### Week 2 (June 14-20): Foundation
- JWT authentication (Module 1)
- Role-based access control
- Mock ERP API server
- Basic LangChain chain
- Prompt library design
- ChromaDB setup

### Week 3 (June 21-27): Core Features
- Student features (attendance, results, timetable)
- ERP API connectors
- RAG pipeline for knowledge base
- Conversation memory (Module 5)
- Unit tests

### Week 4 (June 28 - July 4): Advanced Features
- Faculty features
- Admin features
- Study plan generator (Module 4)
- Fee & assignment queries
- Integration testing

### Week 5 (July 5-11): Integration & UI
- Chat UI (web-based)
- WebSocket/streaming
- Full module integration
- Cross-team coordination
- End-to-end testing

### Week 6 (July 12-18): Security & Testing
- Security testing (data leakage)
- Penetration testing
- Performance optimization (< 3s response)
- Prompt accuracy testing (90%+ target)
- Audit log verification

### Week 7 (July 19-25): Documentation & Polish
- Write all documentation
- Test with open-source LLM (Phase 2)
- UI polish
- Code cleanup
- Demo preparation

### Week 8 (July 26-31): Final Demo
- Final integration with real ERP (if ready)
- Final testing
- Demo rehearsal
- **Final presentation to CEO**
- Code handover

---

## 14. Success Criteria

Our project will be evaluated on:

| Criteria | Target | How to Test |
|----------|--------|------------|
| Response Time | < 3 seconds | Measure with timer |
| Accuracy | 90%+ | Test 100 questions |
| Data Leakage | 0% | Try accessing other users' data |
| ERP Integration | Successful | API calls return correct data |
| Role-Based Security | Implemented | Each role sees only their data |
| Audit Logging | Complete | Every request is logged |
| Conversation Context | Working | Follow-up questions work |
| Knowledge Base | Accurate | Policy questions answered correctly |

---

## 15. Out of Scope

We do NOT build:
- The ERP system itself (frontend, backend, or database)
- Mobile app
- Data analytics dashboards
- User registration/login system (ERP handles this)
- Any write operations (we are READ-ONLY)

---

## 16. Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Git
- VS Code (recommended)
- OpenAI API key (will be provided)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/technify-ai/taia.git
cd technify-ai-assistant

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
copy .env.example .env
# Edit .env with your API keys

# 6. Generate test data
python scripts/generate_data.py

# 7. Run the server
uvicorn app.main:app --reload

# 8. Open API docs
# Visit: http://localhost:8000/docs
```

### Verify Installation

After running the server, visit http://localhost:8000/docs — you should see the Swagger UI with available endpoints.

---

## Contact

- **Team Lead:** [Your Name] — [Your Phone/Email]
- **CEO:** [CEO Name]
- **Internship Coordinator:** [Coordinator Name]

---

*This document is the single source of truth for our project. All team members must read it completely.*
