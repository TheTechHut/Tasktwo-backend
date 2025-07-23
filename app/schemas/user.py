from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"


class User(BaseModel):
    username: str
    role: Role
