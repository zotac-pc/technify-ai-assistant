"""Mock ERP Server — simulates the Laravel ERP backend for development.
Run with: uvicorn mock_erp.main:app --port 8001 --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mock_erp.routes import router

app = FastAPI(title="Mock Technify ERP", version="1.0.0", docs_url="/docs")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"service": "Mock Technify ERP", "status": "running"}
