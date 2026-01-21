from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import schemas, services, utils
from app.auth.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()  # For extracting Bearer tokens

# Dependency to get current authenticated user
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts and verifies JWT token from Authorization header.
    Returns the current user if token is valid.
    Usage: user = Depends(get_current_user) in any protected route.
    """
    token = credentials.credentials
    payload = utils.verify_token(token)
    
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = services.AuthService.get_user_by_id(db, user_id)
    return user

@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    - Validates email format and password strength automatically via Pydantic
    - Checks for duplicate email/username
    - Hashes password before storage
    """
    user = services.AuthService.create_user(db, user_data)
    return user

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.
    Returns access token (30 min) and refresh token (7 days).
    """
    user = services.AuthService.authenticate_user(db, login_data)
    
    # Create tokens with user data
    token_data = {"user_id": user.id, "email": user.email}
    access_token = utils.create_access_token(token_data)
    refresh_token = utils.create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get new access token using refresh token.
    Allows users to stay logged in without re-entering password.
    """
    token = credentials.credentials
    payload = utils.verify_token(token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("user_id")
    user = services.AuthService.get_user_by_id(db, user_id)
    
    # Generate new tokens
    token_data = {"user_id": user.id, "email": user.email}
    access_token = utils.create_access_token(token_data)
    refresh_token = utils.create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    Protected route - requires valid access token.
    """
    return current_user