from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID

KEN_ID = UUID("11111111-1111-1111-1111-111111111111")
BARBIE_ID = UUID("22222222-2222-2222-2222-222222222222")
ADMIN_ID = UUID("33333333-3333-3333-3333-333333333333")

fake_users_db = {
    "ken": {"username": "ken", "role": "customer", "id": str(KEN_ID)},
    "barbie": {"username": "barbie", "role": "agent", "id": str(BARBIE_ID)},
    "admin": {"username": "admin", "role": "admin", "id": str(ADMIN_ID)}
}

# JWT settings
SECRET_KEY = "secret_for_demo_only"  # NEVER use this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 token model
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(username=username, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")

def require_role(role: str):
    def dependency(user: TokenData = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return dependency
