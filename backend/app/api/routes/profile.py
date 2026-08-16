from fastapi import APIRouter, Depends

from app.security.oauth2 import get_current_user
from app.services.profile_service import fetch_profile

router = APIRouter()


@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return fetch_profile(current_user["email"])