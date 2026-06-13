from fastapi import Header, HTTPException
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-from-erp")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def create_token(user_id: str, role: str, name: str, department: str, email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "sub": user_id,
        "role": role,
        "name": name,
        "department": department,
        "email": email,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Yeh function incoming request se user ka role aur ID check karega
def verify_user_access(x_user_role: str = Header(None), x_user_id: str = Header(None)):
    if not x_user_role or not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication details missing!")
    
    return {"role": x_user_role, "user_id": x_user_id}