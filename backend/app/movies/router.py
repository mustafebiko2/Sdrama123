from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.db.session import get_db
from app.shared.files import save_upload
from app.shared.models import Movie, Subtitle
from app.shared.schemas import MovieCreate, MovieRead, MovieUpdate, SubtitleRead

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("", response_model=list[MovieRead])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).order_by(Movie.created_at.desc()).all()


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.patch("/{movie_id}", response_model=MovieRead, dependencies=[Depends(require_admin)])
def update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie


@router.patch("/{movie_id}/publish", response_model=MovieRead, dependencies=[Depends(require_admin)])
def publish_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.status = "published"
    db.commit()
    db.refresh(movie)
    return movie


@router.post("/{movie_id}/poster", response_model=MovieRead, dependencies=[Depends(require_admin)])
def upload_movie_poster(movie_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.poster_path = save_upload(file, "posters/movies")
    db.commit()
    db.refresh(movie)
    return movie


@router.post("/{movie_id}/video", response_model=MovieRead, dependencies=[Depends(require_admin)])
def upload_movie_video(movie_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.video_path = save_upload(file, "videos/movies")
    db.commit()
    db.refresh(movie)
    return movie


@router.post("/{movie_id}/subtitles", response_model=SubtitleRead, dependencies=[Depends(require_admin)])
def upload_movie_subtitle(
    movie_id: int,
    language: str = "English",
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    subtitle = Subtitle(movie_id=movie_id, language=language, file_path=save_upload(file, "subtitles/movies"))
    db.add(subtitle)
    db.commit()
    db.refresh(subtitle)
    return subtitle
