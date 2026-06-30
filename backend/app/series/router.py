from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.db.session import get_db
from app.shared.files import save_upload
from app.shared.models import Episode, Season, Series, Subtitle
from app.shared.schemas import EpisodeCreate, EpisodeRead, EpisodeUpdate, SeasonCreate, SeasonRead, SeriesCreate, SeriesRead, SeriesUpdate, SubtitleRead

router = APIRouter(prefix="/series", tags=["Series"])


@router.get("", response_model=list[SeriesRead])
def list_series(db: Session = Depends(get_db)):
    return db.query(Series).order_by(Series.created_at.desc()).all()


@router.post("", response_model=SeriesRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_series(payload: SeriesCreate, db: Session = Depends(get_db)):
    series = Series(**payload.model_dump())
    db.add(series)
    db.commit()
    db.refresh(series)
    return series


@router.patch("/{series_id}", response_model=SeriesRead, dependencies=[Depends(require_admin)])
def update_series(series_id: int, payload: SeriesUpdate, db: Session = Depends(get_db)):
    series = db.get(Series, series_id)
    if series is None:
        raise HTTPException(status_code=404, detail="Series not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(series, key, value)
    db.commit()
    db.refresh(series)
    return series


@router.patch("/{series_id}/publish", response_model=SeriesRead, dependencies=[Depends(require_admin)])
def publish_series(series_id: int, db: Session = Depends(get_db)):
    series = db.get(Series, series_id)
    if series is None:
        raise HTTPException(status_code=404, detail="Series not found")
    series.status = "published"
    db.commit()
    db.refresh(series)
    return series


@router.post("/{series_id}/poster", response_model=SeriesRead, dependencies=[Depends(require_admin)])
def upload_series_poster(series_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    series = db.get(Series, series_id)
    if series is None:
        raise HTTPException(status_code=404, detail="Series not found")
    series.poster_path = save_upload(file, "posters/series")
    db.commit()
    db.refresh(series)
    return series


@router.post("/{series_id}/seasons", response_model=SeasonRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_season(series_id: int, payload: SeasonCreate, db: Session = Depends(get_db)):
    if db.get(Series, series_id) is None:
        raise HTTPException(status_code=404, detail="Series not found")
    season = Season(series_id=series_id, **payload.model_dump())
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


@router.get("/{series_id}/seasons", response_model=list[SeasonRead])
def list_seasons(series_id: int, db: Session = Depends(get_db)):
    return db.query(Season).filter(Season.series_id == series_id).order_by(Season.number).all()


@router.post("/seasons/{season_id}/episodes", response_model=EpisodeRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_episode(season_id: int, payload: EpisodeCreate, db: Session = Depends(get_db)):
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")
    episode = Episode(season_id=season_id, **payload.model_dump())
    db.add(episode)
    db.commit()
    db.refresh(episode)
    return episode


@router.patch("/episodes/{episode_id}", response_model=EpisodeRead, dependencies=[Depends(require_admin)])
def update_episode(episode_id: int, payload: EpisodeUpdate, db: Session = Depends(get_db)):
    episode = db.get(Episode, episode_id)
    if episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(episode, key, value)
    db.commit()
    db.refresh(episode)
    return episode


@router.patch("/episodes/{episode_id}/publish", response_model=EpisodeRead, dependencies=[Depends(require_admin)])
def publish_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = db.get(Episode, episode_id)
    if episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    episode.status = "published"
    db.commit()
    db.refresh(episode)
    return episode


@router.post("/episodes/{episode_id}/poster", response_model=EpisodeRead, dependencies=[Depends(require_admin)])
def upload_episode_poster(episode_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    episode = db.get(Episode, episode_id)
    if episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    episode.poster_path = save_upload(file, "posters/episodes")
    db.commit()
    db.refresh(episode)
    return episode


@router.post("/episodes/{episode_id}/video", response_model=EpisodeRead, dependencies=[Depends(require_admin)])
def upload_episode_video(episode_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    episode = db.get(Episode, episode_id)
    if episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    episode.video_path = save_upload(file, "videos/episodes")
    db.commit()
    db.refresh(episode)
    return episode


@router.post("/episodes/{episode_id}/subtitles", response_model=SubtitleRead, dependencies=[Depends(require_admin)])
def upload_episode_subtitle(
    episode_id: int,
    language: str = "English",
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    episode = db.get(Episode, episode_id)
    if episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    subtitle = Subtitle(episode_id=episode_id, language=language, file_path=save_upload(file, "subtitles/episodes"))
    db.add(subtitle)
    db.commit()
    db.refresh(subtitle)
    return subtitle
