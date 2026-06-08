from fastapi import Depends, HTTPException
from app.auth.jwt_handler import verify_user_access

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(verify_user_access)):
        if user["role"] not in self.allowed_roles:
            # Urdu message ko English se badal diya
            raise HTTPException(
                status_code=403, 
                detail="Access denied. You do not have permission to access this resource!"
            )
        return user