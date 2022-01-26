from sqlalchemy.orm import Session

from . import models, schemas


def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.uuid == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, emp: schemas.EmployeeCreate, commerce_id: int):
    db_employee = models.Employee(**emp.dict(), commerce_id=commerce_id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_db, employee: schemas.EmployeeCreate):
    for key, value in employee.dict().items():
        setattr(employee_db, key, value)
    db.add(employee_db)
    db.commit()
    db.refresh(employee_db)
    return employee_db

def delete_employee(db: Session, employee_db):
    db.delete(employee_db)
    db.commit()
    return

def get_commerce_by_uuid(db: Session, api_key: str):
    return db.query(models.Commerce).filter(models.Commerce.api_key == api_key).first()