from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.shared.models import Episode, Favorite, Movie, View
from app.shared.schemas import FavoriteCreate, ViewCreate

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/views", status_code=status.HTTP_201_CREATED)
def record_view(payload: ViewCreate, db: Session = Depends(get_db)):
    if payload.movie_id is None and payload.episode_id is None:
        raise HTTPException(status_code=400, detail="movie_id or episode_id is required")
    view = View(**payload.model_dump())
    db.add(view)
    db.commit()
    return {"id": view.id, "message": "View recorded"}


@router.post("/favorites", status_code=status.HTTP_201_CREATED)
def add_favorite(payload: FavoriteCreate, db: Session = Depends(get_db)):
    if payload.movie_id is None and payload.episode_id is None:
        raise HTTPException(status_code=400, detail="movie_id or episode_id is required")
    favorite = Favorite(**payload.model_dump())
    db.add(favorite)
    db.commit()
    return {"id": favorite.id, "message": "Favorite saved"}


@router.delete("/favorites/{favorite_id}")
def remove_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.get(Favorite, favorite_id)
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return {"message": "Favorite removed"}


@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    movie_views = (
        db.query(Movie.title, func.count(View.id).label("views"))
        .join(View, View.movie_id == Movie.id)
        .group_by(Movie.id)
        .order_by(func.count(View.id).desc())
        .limit(10)
        .all()
    )
    episode_views = (
        db.query(Episode.title, func.count(View.id).label("views"))
        .join(View, View.episode_id == Episode.id)
        .group_by(Episode.id)
        .order_by(func.count(View.id).desc())
        .limit(10)
        .all()
    )
    return {
        "total_views": db.query(View).count(),
        "total_favorites": db.query(Favorite).count(),
        "top_movies": [{"title": title, "views": views} for title, views in movie_views],
        "top_episodes": [{"title": title, "views": views} for title, views in episode_views],
    }
