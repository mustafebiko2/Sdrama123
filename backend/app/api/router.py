from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.movies.router import router as movies_router
from app.series.router import router as series_router
from app.genres.router import router as genres_router
from app.categories.router import router as categories_router
from app.subtitles.router import router as subtitles_router
from app.analytics.router import router as analytics_router
from app.dashboard.router import router as dashboard_router
from app.settings.router import router as settings_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(movies_router)
api_router.include_router(series_router)
api_router.include_router(genres_router)
api_router.include_router(categories_router)
api_router.include_router(subtitles_router)
api_router.include_router(analytics_router)
api_router.include_router(dashboard_router)
api_router.include_router(settings_router)
