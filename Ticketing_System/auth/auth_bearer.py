
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # OAuth2 flow for password-based auth
from sqlalchemy.orm import Session

# Custom JWT token decoder
from Ticketing_System.auth.auth_handler import decode_access_token
from Ticketing_System.database import get_db
from Ticketing_System.models import User


# Define the OAuth2 scheme to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# FastAPI will look for a bearer token in the "Authorization" header (e.g., "Bearer <token>")

# Dependency to retrieve the current user from a valid token
def get_current_user(token: str = Depends(Depends(oauth2_scheme)), db: Session = Depends(get_db)) -> User: #Depends(oauth2_scheme)
    """
    Validates the JWT token and retrieves the corresponding user from the database.

    Args:
        token: The JWT access token from the Authorization header.
        db: A database session, injected by FastAPI.

    Returns:
        The authenticated User object.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """

    # Standard exception to raise when authentication fails
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},  # This helps clients know how to authenticate
    )

    # Decode and validate the JWT token
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception  # Token is invalid or expired

    # Retrieve the user ID from the token payload
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise credentials_exception  # No user found for the given ID

    return user  # Authenticated user returned for downstream use