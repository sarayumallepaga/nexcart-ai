from fastapi import HTTPException

from app.repositories.profile_repository import get_profile


def fetch_profile(email: str):
    user = get_profile(email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user