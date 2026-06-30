from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import require_admin
from app.db.session import get_db
from app.shared.models import Setting
from app.shared.schemas import SettingRead, SettingWrite

router = APIRouter(prefix="/settings", tags=["Settings"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[SettingRead])
def list_settings(db: Session = Depends(get_db)):
    return db.query(Setting).order_by(Setting.key).all()


@router.put("/{key}", response_model=SettingRead)
def upsert_setting(key: str, payload: SettingWrite, db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.key == key).first()
    if setting is None:
        setting = Setting(key=key, value=payload.value)
        db.add(setting)
    else:
        setting.value = payload.value
    db.commit()
    db.refresh(setting)
    return setting
