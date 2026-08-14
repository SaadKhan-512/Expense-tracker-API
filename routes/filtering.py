from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Date, cast, and_
from sqlalchemy.orm import Session
import database, models, schemas
from datetime import date
from dateutil.relativedelta import relativedelta

router = APIRouter(prefix="/api/filtering", tags=["Filtering"])

def validate_date_range(start_date, end_date):
    # Trimming year/month/day from start and end date
    start_year , start_month , start_day  = start_date.split("-")
    end_year , end_month , end_day = end_date.split("-")

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

@router.post("/date-range")
def get_expenses_by_date_range(date_range: schemas.date_schema, db: Session = Depends(database.get_db)):
    if validate_date_range(date_range.start, date_range.end) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Issue in you given dates.")
    
    query = db.query(models.Expenses).filter(
        cast(models.Expenses.created_at, Date) >= date_range.start,
        cast(models.Expenses.created_at, Date) <= date_range.end
    ).all()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expenses not found in given range.")

    return query

@router.get("/previous-month")
def get_previous_month_expenses(db: Session = Depends(database.get_db)):
    one_month_ago = date.today() - relativedelta(months=1)

    expenses = db.query(models.Expenses).filter(
            cast(models.Expenses.created_at, Date) >= one_month_ago,
            cast(models.Expenses.created_at, Date) <= date.today()
        ).all()
    
    return expenses

@router.get("/previous-3-months")
def get_previous_3_months_expenses(db: Session = Depends(database.get_db)):
    one_month_ago = date.today() - relativedelta(months=3)
    print(relativedelta(months=3))
    expenses = db.query(models.Expenses).filter(
            cast(models.Expenses.created_at, Date) >= one_month_ago,
            cast(models.Expenses.created_at, Date) <= date.today()
        ).all()
        
    return expenses