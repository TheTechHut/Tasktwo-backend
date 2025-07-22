from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel

# Import local modules
from Ticketing_System.database import get_db
from Ticketing_System.models import User
from Ticketing_System.auth.auth_handler import create_access_token
from Ticketing_System.testauth import get_current_user
from Ticketing_System.routers import tickets

app = FastAPI(
    title="Ticketing System API",
    description="REST API for customers, agents, and admins to manage support tickets.",
    version="1.0.0"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#login
@app.post("/login", summary="User login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}

#  router
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])



