from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserRegister
from app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):
    return register_user(user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)