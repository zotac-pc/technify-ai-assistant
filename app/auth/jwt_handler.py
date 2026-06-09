from fastapi import Header, HTTPException

# Yeh function incoming request se user ka role aur ID check karega
def verify_user_access(x_user_role: str = Header(None), x_user_id: str = Header(None)):
    if not x_user_role or not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication details missing!")
    
    return {"role": x_user_role, "user_id": x_user_id}