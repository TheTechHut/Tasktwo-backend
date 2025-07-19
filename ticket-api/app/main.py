from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import create_token, fake_users
from app.api import tickets

app = FastAPI()

app.include_router(tickets.router, prefix="/api")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password  # not validated for now

    user = fake_users.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")

    # Optional: you can add fake password check if you want
    token = create_token(username)
    return {"access_token": token, "token_type": "bearer"}
