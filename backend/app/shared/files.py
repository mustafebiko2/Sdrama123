from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


def save_upload(file: UploadFile, folder: str) -> str:
    settings = get_settings()
    upload_root = Path(settings.upload_dir)
    target_dir = upload_root / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename or "").suffix
    filename = f"{uuid4().hex}{suffix}"
    target_path = target_dir / filename

    with target_path.open("wb") as output:
        output.write(file.file.read())

    return str(target_path)
