from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.schemas.user import User, Role
from app.database import SessionLocal

# JWT settings (should match auth.py)
SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

# Extracts token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Dependency: get a database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency: decode JWT and return the current user


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise JWTError()
        return User(username=username, role=role)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# Dependency factory: restricts access to certain roles


def require_role(required_roles: list[Role]):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_dependency
