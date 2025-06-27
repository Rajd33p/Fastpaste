from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

@router.post("/paste", response_model=schemas.PasteResponse)
def create_paste(
        paste : schemas.PasteCreate,
        db: Session = Depends(database.get_db)

):
    try:
        new_paste = crud.create_paste(db, paste)
        return new_paste
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{slug}", response_model=schemas.PasteResponse)
def read_paste(slug: str, db: Session = Depends(database.get_db)):
    paste = crud.get_paste_by_slug(db, slug)
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found or expired")
    return paste
