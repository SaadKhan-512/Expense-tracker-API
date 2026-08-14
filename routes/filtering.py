from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Date, cast, and_
from sqlalchemy.orm import Session
import database, models, schemas

router = APIRouter(prefix="/api/filtering", tags=["Filtering"])

def validate_dates(starting_date, ending_date):
    # Trimming year/month/day from start and end date
    start_year , start_month , start_day  =starting_date.split("-")
    end_year , end_month , end_day = ending_date.split("-")

    # Checking year range
    if int(start_year) < 2026 or int(start_year) > 2100 or int(end_year)< 2026 or int(end_year)> 2100:
        return False
    
    # Check month range
    if int(start_month) < 1 or int(start_month) > 12 or int(end_month) < 1 or int(end_month) > 12:
        return False
    
    # Check days range
    if int(start_day) < 1 or int(start_day) > 31 or int(end_day) < 1 or int(end_day) > 31:
        return False
 

    return True

@router.post("")
def get_by_duration_of_time(dates: schemas.date_schema, db: Session = Depends(database.get_db)):
    if validate_dates(dates.start, dates.end) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Issue in you given dates.")
    
    query = db.query(models.Expenses).filter(
        cast(models.Expenses.created_at, Date) >= dates.start,
        cast(models.Expenses.created_at, Date) <= dates.end
    ).all()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expenses not found in given range.")

    return query