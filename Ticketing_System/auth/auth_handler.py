from datetime import datetime, timedelta
from jose import jwt, JWTError  # 'jose' is used to encode/decode JWTs

# Secret key and algorithm used for encoding/decoding tokens
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"  # Common HMAC algorithm used for symmetric key JWTs
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token validity duration

# Function to create a JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT token with an expiration timestamp.

    Args:
        data (dict): The payload to include in the token (e.g., user ID).
        expires_delta (timedelta): Custom expiration time.

    Returns:
        str: Encoded JWT token.
    """
    # Copy payload data to avoid modifying original
    to_encode = data.copy()

    # Set expiration time (default: 60 minutes from now)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # Add the expiration to the token payload
    to_encode.update({"exp": expire})

    # Encode the token using the secret key and algorithm
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode and validate a JWT token
def decode_access_token(token: str):
    """
    Decodes a JWT token and returns the payload if valid.

    Args:
        token (str): The JWT token string.

    Returns:
        dict or None: The decoded payload, or None if invalid or expired.
    """
    try:
        # Attempt to decode the token with the given key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # If the token is invalid, tampered, or expired, return None
        return None