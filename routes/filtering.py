from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
import database, models, schemas

router = APIRouter(prefix="/api/filtering", tags=["Filtering"])


@router.post("")
def get_by_duration_of_time(dates: schemas.date_schema, db: Session = Depends(database.get_db)):
    query = db.query(models.Expenses).filter(cast(models.Expenses.created_at, Date) == dates.start).all()

    return query