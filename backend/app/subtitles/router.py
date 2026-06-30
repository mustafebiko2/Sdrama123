from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.shared.models import Subtitle
from app.shared.schemas import SubtitleRead

router = APIRouter(prefix="/subtitles", tags=["Subtitles"])


@router.get("", response_model=list[SubtitleRead])
def list_subtitles(db: Session = Depends(get_db)):
    return db.query(Subtitle).order_by(Subtitle.id.desc()).all()
