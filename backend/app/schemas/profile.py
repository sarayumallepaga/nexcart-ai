from pydantic import BaseModel


class ProfileResponse(BaseModel):
    name: str
    email: str