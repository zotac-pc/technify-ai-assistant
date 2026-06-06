# Architecture Document — Technify Academic AI Assistant (TAIA)
## Deliverable #1 — AI Team 1

**Version:** 1.0  
**Date:** June 7, 2026  
**Author:** Team Lead, AI Team 1  

---

## 1. High-Level Architecture

The Technify Academic AI Assistant is a **standalone microservice** that integrates with the Technify University ERP through secure REST APIs.

```
+===============================================================+
|                    TECHNIFY UNIVERSITY ERP                      |
|                                                                 |
|  +-----------+  +-----------+  +---------------------------+   |
|  | React.js  |  | Flutter   |  | Laravel Backend           |   |
|  | Frontend  |  | Mobile    |  | (PHP)                     |   |
|  | (Next.js) |  | App       |  |                           |   |
|  +-----+-----+  +-----+-----+  | +-------+ +-----------+  |   |
|        |              |         | | REST  | | PostgreSQL|  |   |
|        +--------------+---------+-+ APIs  | | Database  |  |   |
|                                   +---+---+ +-----+-----+  |   |
|                                       |           |         |   |
+=======================================|===========|=========+   |
                                        |           |             |
                                   REST API     Database          |
                                   (JSON)      (Internal)         |
                                        |                         |
+=======================================|=========================+
|                 AI MICROSERVICE        |                         |
|                                        |                         |
|  +---+   +---------+   +----------+   |   +------------------+ |
|  |   |   | FastAPI |   | LangChain|   |   | ChromaDB         | |
|  | U |-->| Gateway |-->| Engine   |---+-->| (Vector Store)   | |
|  | S |   |         |   |          |       |                  | |
|  | E |   | - Auth  |   | - Chains |       | University Docs: | |
|  | R |   | - RBAC  |   | - Tools  |       | - Policies       | |
|  |   |   | - Audit |   | - Memory |       | - Rules          | |
|  +---+   +---------+   +----+-----+       | - Calendar       | |
|                              |             +------------------+ |
|                         +----v-----+                            |
|                         |   LLM    |                            |
|                         | GPT-4o   |                            |
|                         | /Llama   |                            |
|                         +----------+                            |
+================================================================+
```

---

## 2. Component Details

### 2.1 FastAPI Gateway (API Layer)

**Responsibility:** Receives all incoming requests, handles authentication, routes to appropriate service.

| Component | File | Purpose |
|-----------|------|---------|
| Main App | `app/main.py` | FastAPI application entry point |
| Chat Route | `app/api/routes/chat.py` | `POST /api/v1/chat` — main chat endpoint |
| Health Route | `app/api/routes/health.py` | `GET /health` — service health check |
| Admin Route | `app/api/routes/admin.py` | Admin-only endpoints |
| Auth Middleware | `app/auth/jwt_handler.py` | JWT token validation |
| RBAC | `app/auth/rbac.py` | Role-based permission checking |
| Audit Logger | `app/api/middleware/audit_log.py` | Request/response logging |

### 2.2 LangChain Engine (AI Layer)

**Responsibility:** Processes user questions, determines intent, calls appropriate tools, generates responses.

| Component | File | Purpose |
|-----------|------|---------|
| AI Service | `app/services/ai_service.py` | Main orchestrator |
| Student Chain | `app/chains/student_chain.py` | Student question handling |
| Faculty Chain | `app/chains/faculty_chain.py` | Faculty question handling |
| Admin Chain | `app/chains/admin_chain.py` | Admin question handling |
| Prompt Templates | `app/prompts/*.py` | All prompt templates |

### 2.3 ERP Connector (Integration Layer)

**Responsibility:** Communicates with the ERP backend APIs securely.

| Component | File | Purpose |
|-----------|------|---------|
| ERP Connector | `app/services/erp_connector.py` | HTTP client for ERP APIs |
| Mock ERP | `mock_erp/main.py` | Simulated ERP for development |

### 2.4 Knowledge Base (RAG Layer)

**Responsibility:** Stores and retrieves university policy documents.

| Component | File | Purpose |
|-----------|------|---------|
| KB Service | `app/services/knowledge_base.py` | ChromaDB operations |
| Documents | `data/documents/` | Source policy files |
| Vector Store | `data/vector_store/` | ChromaDB persistent storage |

---

## 3. Request Processing Flow

```
User Message: "What is my attendance in Web Engineering?"

Step 1: [FastAPI Gateway]
        - Receive POST /api/v1/chat
        - Extract JWT from Authorization header
        - Validate JWT token (check signature, expiry)
        - Extract: user_id="STU-0042", role="student"
        - Check: Does student role have permission to query attendance? YES
        - Log request to audit log

Step 2: [LangChain Engine]
        - Route to Student Chain (based on role)
        - Parse intent: "attendance_query"
        - Extract entities: course="Web Engineering"
        - Check conversation memory for context

Step 3: [ERP Connector]
        - Call: GET {ERP_URL}/api/v1/student/STU-0042/attendance
        - Headers: Authorization: Bearer {JWT_TOKEN}
        - Receive: JSON response with attendance data
        - Filter for "Web Engineering" course

Step 4: [LangChain Engine]
        - Format data into prompt
        - Send to LLM (GPT/Llama)
        - LLM generates human-readable response

Step 5: [FastAPI Gateway]
        - Return response to user
        - Log response to audit log
        - Update conversation memory

Response: "Your attendance in Web Engineering (CS-301) is 78%.
           You have attended 25 out of 32 classes."
```

---

## 4. Security Architecture

```
+------------------+
| Incoming Request |
+--------+---------+
         |
    +----v----+
    | Extract |
    | JWT     |
    | Token   |
    +----+----+
         |
    +----v-----------+     +----------+
    | Validate JWT   |---->| REJECT   |
    | - Signature    | NO  | (401)    |
    | - Expiry       |     +----------+
    | - Issuer       |
    +----+-----------+
         | YES (Valid)
    +----v-----------+
    | Extract Role   |
    | & User ID      |
    +----+-----------+
         |
    +----v-----------+     +----------+
    | Check RBAC     |---->| REJECT   |
    | Permission     | NO  | (403)    |
    +----+-----------+     +----------+
         | YES (Allowed)
    +----v-----------+
    | Log to Audit   |
    +----+-----------+
         |
    +----v-----------+
    | Process Query  |
    +----------------+
```

### Role Permissions Matrix

| Permission | Student | Faculty | Admin | Finance | Exam Officer |
|-----------|---------|---------|-------|---------|-------------|
| Own attendance | Yes | - | - | - | - |
| Own results | Yes | - | - | - | - |
| Own fees | Yes | - | - | - | - |
| Own timetable | Yes | - | - | - | - |
| Course students | - | Yes (own courses) | - | - | - |
| Course stats | - | Yes (own courses) | - | - | - |
| All students stats | - | - | Yes | - | - |
| Fee collection stats | - | - | Yes | Yes | - |
| Exam statistics | - | - | Yes | - | Yes |
| Department stats | - | - | Yes | - | - |

---

## 5. API Endpoints

### Our Service APIs (What we expose)

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|--------------|
| `GET` | `/` | Root / service info | No |
| `GET` | `/health` | Health check | No |
| `POST` | `/api/v1/chat` | Send message to AI | Yes (JWT) |
| `GET` | `/api/v1/chat/history/{session_id}` | Get chat history | Yes (JWT) |
| `DELETE` | `/api/v1/chat/history/{session_id}` | Clear chat history | Yes (JWT) |
| `GET` | `/api/v1/admin/audit-logs` | View audit logs | Yes (Admin only) |
| `GET` | `/api/v1/admin/stats` | Service statistics | Yes (Admin only) |

### Chat Request Format

```json
POST /api/v1/chat
Headers:
  Authorization: Bearer <JWT_TOKEN>
  Content-Type: application/json

Body:
{
  "message": "What is my attendance in Web Engineering?",
  "session_id": "sess_abc123"  // optional, for conversation continuity
}
```

### Chat Response Format

```json
{
  "response": "Your attendance in Web Engineering (CS-301) is 78%...",
  "session_id": "sess_abc123",
  "response_time_ms": 1250,
  "sources": ["erp_api"],
  "metadata": {
    "intent": "attendance_query",
    "entities": {"course": "Web Engineering"}
  }
}
```

---

## 6. ERP APIs (What we consume)

These are the APIs we need the Laravel team to build:

### Student APIs
```
GET /api/v1/student/{student_id}                    -> Student profile
GET /api/v1/student/{student_id}/attendance          -> All attendance records
GET /api/v1/student/{student_id}/attendance/{course}  -> Course-specific attendance
GET /api/v1/student/{student_id}/results             -> All exam results
GET /api/v1/student/{student_id}/gpa                 -> GPA calculation
GET /api/v1/student/{student_id}/courses             -> Registered courses
GET /api/v1/student/{student_id}/timetable           -> Weekly timetable
GET /api/v1/student/{student_id}/assignments         -> Assignment status
GET /api/v1/student/{student_id}/fees                -> Fee records
```

### Faculty APIs
```
GET /api/v1/faculty/{faculty_id}/courses              -> Assigned courses
GET /api/v1/faculty/{faculty_id}/course/{course_id}/students    -> Student list
GET /api/v1/faculty/{faculty_id}/course/{course_id}/attendance  -> Attendance report
GET /api/v1/faculty/{faculty_id}/assignments          -> Ungraded assignments
```

### Admin APIs
```
GET /api/v1/admin/statistics/students     -> Enrollment numbers
GET /api/v1/admin/statistics/admissions   -> Admission data
GET /api/v1/admin/statistics/fees         -> Fee collection data
GET /api/v1/admin/statistics/departments  -> Department performance
```

---

## 7. Data Flow Diagram

```
                        +--------+
                        | User   |
                        +---+----+
                            |
                      "What is my GPA?"
                            |
                    +-------v--------+
                    | POST /chat     |
                    | JWT: eyJhbG... |
                    +-------+--------+
                            |
                +-----------v-----------+
                | FASTAPI GATEWAY       |
                |                       |
                | 1. Validate JWT       |
                | 2. user=STU-0042      |
                | 3. role=student       |
                | 4. Log to audit       |
                +-----------+-----------+
                            |
                +-----------v-----------+
                | LANGCHAIN ENGINE      |
                |                       |
                | 1. Detect intent:     |
                |    "gpa_query"        |
                | 2. No course filter   |
                | 3. Select tool:       |
                |    get_student_gpa()  |
                +-----------+-----------+
                            |
              +-------------v--------------+
              | ERP CONNECTOR              |
              |                            |
              | GET /api/v1/student/       |
              |     STU-0042/gpa           |
              | Auth: Bearer eyJhbG...     |
              +-------------+--------------+
                            |
                     +------v------+
                     | ERP Response|
                     | {           |
                     |  cgpa: 3.45 |
                     |  semester:6 |
                     | }           |
                     +------+------+
                            |
              +-------------v--------------+
              | LLM (GPT / Llama)          |
              |                            |
              | Prompt: "Student STU-0042  |
              | has CGPA 3.45 in semester  |
              | 6. Generate a friendly     |
              | response about their GPA." |
              +-------------+--------------+
                            |
                     +------v------+
                     | AI Response |
                     | "Your CGPA  |
                     |  is 3.45    |
                     |  (A grade)" |
                     +------+------+
                            |
                    +-------v--------+
                    | Return to User |
                    +----------------+
```

---

## 8. Deployment Architecture (Future)

```
+------------------------------------------+
|           Cloud (AWS / Azure)            |
|                                          |
|  +------------------+  +--------------+  |
|  | Docker Container |  | Docker       |  |
|  | AI Service       |  | Container    |  |
|  | (FastAPI +       |  | ChromaDB     |  |
|  |  LangChain)      |  |              |  |
|  +--------+---------+  +------+-------+  |
|           |                    |          |
|  +--------v--------------------v-------+ |
|  |        Internal Network             | |
|  +-------------------------------------+ |
|                                          |
+------------------------------------------+
           |
      HTTPS (443)
           |
+----------v-----------+
| Technify ERP Server  |
| (Laravel + React)    |
+----------------------+
```

---

*This document serves as Deliverable #1: Architecture Diagram.*
