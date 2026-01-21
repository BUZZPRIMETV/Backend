from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

# Request Schema for User Signup
class UserCreate(BaseModel):
    email: EmailStr  # Validates email format automatically
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = None

# Request Schema for Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response Schema - What we return to client (no password!)
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  # Allows ORM model conversion

# Token Response after successful login
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Token data stored inside JWT
class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
