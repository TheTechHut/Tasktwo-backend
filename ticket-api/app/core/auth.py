from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Dict
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key and fake users
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

fake_users = {
    "customer1": {"id": "user-customer", "role": "customer"},
    "agent1": {"id": "user-agent", "role": "agent"},
    "admin1": {"id": "user-admin", "role": "admin"}
}


def create_token(username: str):
    user = fake_users.get(username)
    if not user:
        raise Exception("Invalid user")
    to_encode = {"sub": username, "role": user["role"], "id": user["id"]}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: str):
    def role_checker(user: Dict = Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
