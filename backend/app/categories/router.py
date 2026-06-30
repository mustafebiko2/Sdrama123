from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.db.session import get_db
from app.shared.models import Category
from app.shared.schemas import TaxonomyCreate, TaxonomyRead

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[TaxonomyRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()


@router.post("", response_model=TaxonomyRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_category(payload: TaxonomyCreate, db: Session = Depends(get_db)):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
