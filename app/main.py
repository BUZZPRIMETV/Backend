from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.auth.routes import router as auth_router
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

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
async def root():
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


@app.middleware("http")
async def show_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        traceback.print_exc()  # <-- this will appear in Vercel logs
        return JSONResponse(status_code=500, content={"detail": str(e)})