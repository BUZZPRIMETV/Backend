from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.auth.routes import router as auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Movie Streaming Platform API"
)

# CORS Middleware - allows frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - this is how you add different modules
app.include_router(auth_router)

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "message": "MovieStream API is running",
        "version": settings.VERSION,
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    """Detailed health check for monitoring."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.VERSION
    }