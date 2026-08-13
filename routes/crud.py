from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database, models, schemas

router = APIRouter(prefix="/api/expenses", tags=["CRUD"])

@router.post("")
def add_expense(expense: schemas.expenses_schema, db: Session = Depends(database.get_db)):
    new_expense = models.Expenses(**expense.dict())

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return "Expense added successfully."

@router.get("")
def get_expenses(db: Session = Depends(database.get_db)):
    return db.query(models.Expenses).all()

@router.put("/{id}")
def updated_expense(id: int, expense: schemas.expenses_schema, db: Session = Depends(database.get_db)):
    expense_query = db.query(models.Expenses).filter(models.Expenses.id == id).first()

    if not expense_query:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expense_query.name = expense.name
    expense_query.category = expense.category
    expense_query.price = expense.price

    db.commit()
    db.refresh(expense_query)

    return "Expense updated successfully."

@router.delete("/{id}")
def delete_expense(id: int, db: Session = Depends(database.get_db)):
    expense_query = db.query(models.Expenses).filter(models.Expenses.id == id).first()

    if not expense_query:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense_query)
    db.commit()

    return "Expense deletedmmm  cx successfully."