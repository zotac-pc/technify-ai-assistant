# API Guide — Technify Academic AI Assistant
## For ERP Integration & Developer Reference

**Version:** 1.0  
**Base URL:** `http://localhost:8000`  
**Authentication:** JWT Bearer Token (from ERP)  

---

## 1. Service Information

### GET /
Returns service status.

**Request:**
```
GET /
```

**Response (200):**
```json
{
    "service": "Technify Academic AI Assistant (TAIA)",
    "status": "running",
    "version": "0.1.0"
}
```

---

### GET /health
Returns detailed health status of all components.

**Request:**
```
GET /health
```

**Response (200):**
```json
{
    "status": "healthy",
    "components": {
        "api": "up",
        "llm": "connected",
        "vector_db": "connected",
        "erp_api": "connected"
    }
}
```

---

## 2. Chat Endpoint

### POST /api/v1/chat
Main endpoint for sending messages to the AI assistant.

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**
```json
{
    "message": "What is my attendance?",
    "session_id": "sess_abc123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | Yes | The user's question |
| session_id | string | No | Session ID for conversation continuity. If not provided, a new session is created. |

**Response (200):**
```json
{
    "response": "Your overall attendance is 82%. Here's the breakdown by course:\n- Web Engineering: 78%\n- Database Systems: 85%\n- AI: 90%",
    "session_id": "sess_abc123",
    "response_time_ms": 1250,
    "sources": ["erp_api"],
    "metadata": {
        "intent": "attendance_query",
        "role": "student",
        "user_id": "STU-0042"
    }
}
```

**Error Responses:**

*401 Unauthorized (Invalid/expired JWT):*
```json
{
    "detail": "Invalid or expired token"
}
```

*403 Forbidden (Insufficient permissions):*
```json
{
    "detail": "You do not have permission to access this information"
}
```

*500 Internal Server Error:*
```json
{
    "detail": "An error occurred while processing your request"
}
```

---

## 3. Chat History

### GET /api/v1/chat/history/{session_id}
Retrieve conversation history for a session.

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```

**Response (200):**
```json
{
    "session_id": "sess_abc123",
    "messages": [
        {
            "role": "user",
            "content": "What is my attendance?",
            "timestamp": "2026-06-07T10:30:00Z"
        },
        {
            "role": "assistant",
            "content": "Your overall attendance is 82%...",
            "timestamp": "2026-06-07T10:30:02Z"
        }
    ]
}
```

### DELETE /api/v1/chat/history/{session_id}
Clear a conversation session.

**Response (200):**
```json
{
    "message": "Session cleared successfully",
    "session_id": "sess_abc123"
}
```

---

## 4. Admin Endpoints

### GET /api/v1/admin/audit-logs
Get audit logs (Admin only).

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| limit | int | Records per page (default: 50) |
| user_id | string | Filter by user ID |
| role | string | Filter by role |
| date_from | string | Start date (YYYY-MM-DD) |
| date_to | string | End date (YYYY-MM-DD) |

**Response (200):**
```json
{
    "total": 1250,
    "page": 1,
    "limit": 50,
    "logs": [
        {
            "log_id": "LOG-000001",
            "user_id": "STU-0042",
            "role": "student",
            "query": "What is my attendance?",
            "response_type": "attendance_query",
            "timestamp": "2026-06-07T10:30:00Z",
            "response_time_ms": 1250
        }
    ]
}
```

---

## 5. JWT Token Format

The JWT token is issued by the ERP system. Our service validates it.

**Token Payload (decoded):**
```json
{
    "user_id": "STU-0042",
    "role": "student",
    "department": "Computer Science",
    "name": "Ahmed Khan",
    "email": "ahmed.khan@student.technify.edu.pk",
    "iat": 1719300000,
    "exp": 1719345600,
    "iss": "technify-erp"
}
```

**Valid Roles:**
- `student`
- `faculty`
- `admin`
- `finance`
- `exam_officer`
- `department_head`
- `dean`

---

## 6. Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request body |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Endpoint not found |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Internal error |
| 503 | Service Unavailable | LLM or ERP API is down |

---

## 7. Rate Limiting

| Role | Requests/Minute |
|------|----------------|
| Student | 20 |
| Faculty | 30 |
| Admin | 50 |

---

*For questions, contact the AI Team Lead.*
