"""
TAIA Audit Logger Phase 3
Member 5: SQLite Database Logging
Records all AI interactions into a persistent SQLite database.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DB_PATH = ".audit.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, index=True)
    role = Column(String)
    query = Column(String)
    response_type = Column(String)
    response_time = Column(Float)

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

def log_request(user_id: str, role: str, query: str, response_type: str, response_time: float):
    """
    Log a chat interaction to the SQLite database.
    """
    db = SessionLocal()
    try:
        log_entry = AuditLog(
            user_id=user_id,
            role=role,
            query=query,
            response_type=response_type,
            response_time=response_time
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"[TAIA] Audit Logger Error: {e}")
    finally:
        db.close()
