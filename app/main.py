"""
Technify Academic AI Assistant (TAIA)
=====================================
FastAPI Application Entry Point

This is the main entry point for the AI Assistant microservice.
Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import the RoleChecker from our custom authorization module
from app.auth.rbac import RoleChecker  

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Technify Academic AI Assistant (TAIA)",
    description="AI-powered academic assistant integrated with Technify University ERP",
    version="0.1.0",
    docs_url="/docs",          # Swagger UI path
    redoc_url="/redoc",        # ReDoc path
)

# CORS Middleware configuration to allow the ERP frontend to make requests
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================================
# SYSTEM SECURITY RULES (Defining Access Control for Student, Faculty, & Admin)
# =========================================================================
allow_student_and_admin = RoleChecker(["Student", "Admin"])
allow_only_faculty = RoleChecker(["Faculty"])
allow_only_admin = RoleChecker(["Admin"])


# ========== Health Check Endpoints ==========

@app.get("/", tags=["Health"])
async def root():
    # Verify if the application service gateway is up and running
    return {
        "service": "Technify Academic AI Assistant (TAIA)",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    # System health status monitoring endpoint
    return {
        "status": "healthy",
        "components": {
            "api": "up",
            "llm": "not_configured",       # TODO: Check LLM connection
            "vector_db": "not_configured",  # TODO: Check ChromaDB connection
            "erp_api": "not_configured",    # TODO: Check ERP API connection
        },
    }


# ========== Academic & Security Test Endpoints ==========

# 1. Student Route (Accessible by Students and Admins)
@app.get("/api/v1/student/attendance", tags=["Student Features"], dependencies=[Depends(allow_student_and_admin)])
async def get_attendance():
    return {
        "course": "Web Engineering (CS-301)",
        "attendance": "78%",
        "classes_attended": "25 out of 32"
    }


# 2. Faculty Route (Restricted strictly to Faculty members)
@app.get("/api/v1/faculty/at-risk-students", tags=["Faculty Features"], dependencies=[Depends(allow_only_faculty)])
async def get_at_risk_students():
    # Test route to check faculty tracking features
    return {
        "department": "Information Technology",
        "at_risk_count": 4,
        "students": [
            {"id": "STU-0091", "name": "Ali", "attendance": "54%", "reason": "Low Attendance"},
            {"id": "STU-0142", "name": "Sana", "attendance": "62%", "reason": "Ungraded Assignments"}
        ]
    }


# 3. Admin Route (Restricted exclusively to Admin role)
@app.get("/api/v1/admin/fee-report", tags=["Admin Reports"], dependencies=[Depends(allow_only_admin)])
async def get_fee_report():
    return {
        "total_expected": "PKR 425M",
        "collected": "PKR 382.5M",
        "percentage": "90%"
    }


from app.chains.chatbot_chain import generate_chat_response
from fastapi import Request

# ========== Chat Endpoint ==========

@app.post("/api/v1/chat", tags=["Chat"])
async def chat(request: Request, message: dict):
    # Extract session ID from headers or use default
    session_id = request.headers.get("x-session-id", "default_session")
    user_message = message.get("message", "")
    
    if not user_message:
        return {"response": "Please provide a message."}

    # Call LangChain pipeline
    ai_response = await generate_chat_response(session_id, user_message)

    return {
        "response": ai_response,
        "status": "success",
        "note": "Powered by LangChain ConversationBufferMemory"
    }


# ========== Application Startup Event ==========

@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print("Technify Academic AI Assistant (TAIA)")
    print("Service is starting...")
    print(f"Docs available at: http://localhost:{os.getenv('APP_PORT', 8000)}/docs")
    print("=" * 50)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=True,
    )