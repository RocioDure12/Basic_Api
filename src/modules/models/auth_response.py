from pydantic import BaseModel

class AuthResponse(BaseModel):
    access_token:str=None
    refresh_token:str=None
