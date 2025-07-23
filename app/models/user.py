from passlib.context import CryptContext
from app.schemas.user import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {

    "grace": {
        "username": "alice",
        "hashed_password": pwd_context.hash("alice123"),
        "role": Role.CUSTOMER
    },
    "carol": {
        "username": "carol",
        "hashed_password": pwd_context.hash("carol123"),
        "role": Role.ADMIN
    },
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("bob123"),
        "role": Role.AGENT
    }
}
