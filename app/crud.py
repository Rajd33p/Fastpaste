import random
import string
from sqlalchemy.orm import Session
from . import models, schemas
from .models import Paste
from datetime import datetime, timedelta

def generate_slug(length: int = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_paste(db: Session, paste: schemas.PasteCreate) -> models.Paste:
    # Retry slug generation if collision
    for _ in range(5):
        slug = generate_slug()
        if not db.query(models.Paste).filter_by(slug=slug).first():
            break
    else:
        raise Exception("Failed to generate unique slug")

    db_paste = models.Paste(
        slug=slug,
        content=paste.content,
        expires_in=paste.expires_in
    )
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return db_paste

def get_paste_by_slug(db: Session, slug: str) -> Paste | None:
    paste = db.query(Paste).filter_by(slug=slug, is_active=True).first()

    if not paste:
        return None

    if paste.expires_in:
        created_time = paste.created_at
        expires_at = created_time + timedelta(seconds=paste.expires_in)
        if datetime.utcnow() > expires_at:
            # Optionally mark it as inactive for future
            paste.is_active = False
            db.commit()
            return None

    return paste