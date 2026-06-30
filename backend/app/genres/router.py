from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.db.session import get_db
from app.shared.models import Genre
from app.shared.schemas import TaxonomyCreate, TaxonomyRead

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("", response_model=list[TaxonomyRead])
def list_genres(db: Session = Depends(get_db)):
    return db.query(Genre).order_by(Genre.name).all()


@router.post("", response_model=TaxonomyRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_genre(payload: TaxonomyCreate, db: Session = Depends(get_db)):
    genre = Genre(**payload.model_dump())
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre
