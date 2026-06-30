from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.db.session import get_db
from app.shared.models import Episode, Favorite, Movie, Season, Series, Subtitle, User, View

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(require_admin)])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "movies": db.query(Movie).count(),
        "series": db.query(Series).count(),
        "seasons": db.query(Season).count(),
        "episodes": db.query(Episode).count(),
        "subtitles": db.query(Subtitle).count(),
        "views": db.query(View).count(),
        "favorites": db.query(Favorite).count(),
        "published_movies": db.query(Movie).filter(Movie.status == "published").count(),
        "published_episodes": db.query(Episode).filter(Episode.status == "published").count(),
    }
