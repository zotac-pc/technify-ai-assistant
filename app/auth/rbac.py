from fastapi import Depends, HTTPException
from app.auth.jwt_handler import verify_user_access

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(verify_user_access)):
        if user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail="Aapko yeh information dekhne ki ijazat nahi hai!"
            )
        return user