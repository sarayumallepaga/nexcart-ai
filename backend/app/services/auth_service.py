from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)

from app.security.hashing import (
    hash_password,
    verify_password,
)

from app.security.jwt_handler import (
    create_access_token,
)
def register_user(user):
    existing = get_user_by_email(user.email)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
    }

    create_user(user_data)

    return {
        "message": "User registered successfully"
    }
def login_user(form_data: OAuth2PasswordRequestForm):

    db_user = get_user_by_email(form_data.username)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        form_data.password,
        db_user["password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {
            "email": db_user["email"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }