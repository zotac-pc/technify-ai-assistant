"""
Technify Academic AI Assistant (TAIA)
=====================================
FastAPI Application Entry Point

This is the main entry point for the AI Assistant microservice.
Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Technify Academic AI Assistant (TAIA)",
    description="AI-powered academic assistant integrated with Technify University ERP",
    version="0.1.0",
    docs_url="/docs",          # Swagger UI
    redoc_url="/redoc",        # ReDoc
)

# CORS Middleware (allow ERP frontend to call our API)
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Health Check Endpoint ==========
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - confirms the service is running."""
    return {
        "service": "Technify Academic AI Assistant (TAIA)",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "components": {
            "api": "up",
            "llm": "not_configured",       # TODO: Check LLM connection
            "vector_db": "not_configured",  # TODO: Check ChromaDB connection
            "erp_api": "not_configured",    # TODO: Check ERP API connection
        },
    }


# ========== Chat Endpoint (Placeholder) ==========
@app.post("/api/v1/chat", tags=["Chat"])
async def chat(message: dict):
    """
    Main chat endpoint - receives user messages and returns AI responses.
    
    TODO (Week 2-3):
    - Add JWT authentication middleware
    - Add role-based access control
    - Connect to LangChain pipeline
    - Add audit logging
    """
    user_message = message.get("message", "")
    
    return {
        "response": f"AI Assistant is under development. You said: '{user_message}'",
        "status": "placeholder",
        "note": "This endpoint will be connected to LangChain in Week 2-3.",
    }


# ========== Startup Event ==========
@app.on_event("startup")
async def startup_event():
    """Runs when the server starts."""
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
