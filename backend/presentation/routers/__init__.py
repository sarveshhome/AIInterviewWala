from presentation.routers.auth_router import router as auth_router
from presentation.routers.career_router import router as career_router
from presentation.routers.dashboard_router import router as dashboard_router
from presentation.routers.health_router import router as health_router
from presentation.routers.interview_router import router as interview_router
from presentation.routers.resume_router import router as resume_router

routers = [health_router, auth_router, resume_router, interview_router, career_router, dashboard_router]

__all__ = ["routers"]