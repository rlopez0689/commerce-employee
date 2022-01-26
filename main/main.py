from typing import List
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import crud, schemas
from .database import SessionLocal
from .models import Commerce, Employee


app = FastAPI()
security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def curate_employee(employee):
    employee.id = employee.uuid
    return employee


def make_json_response_with_data(data=[], rc=0, msg="Ok"):
    return {"rc": rc, "msg": msg, "data": data}


def get_current_commerce(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    commerce = crud.get_commerce_by_uuid(db, credentials.username)
    if not commerce:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username(api-key)",
            headers={"WWW-Authenticate": "Basic"},
        )
    return commerce.id


@app.get("/employees/", response_model=schemas.BaseEmployeesOutput)
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), commerce_id: HTTPBasicCredentials = Depends(get_current_commerce)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    print(employees)
    return make_json_response_with_data(data=list(map(curate_employee, employees)))


@app.get("/employees/{employee_id}", response_model=schemas.BaseEmployeeOutput)
def read_employee(employee_id: str, db: Session = Depends(get_db), commerce_id: HTTPBasicCredentials = Depends(get_current_commerce)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        return JSONResponse(content={
            "rc": -1001, "msg": 'Please enter a valid id',
        }, status_code=400)
    return make_json_response_with_data(db_employee)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={
        "rc": -1004, "msg": 'Incomplete data',
    }, status_code=400)


@app.post("/employees/", response_model=schemas.BaseEmployeeOutput)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), commerce_id: HTTPBasicCredentials = Depends(get_current_commerce)):
    try:
        return make_json_response_with_data(curate_employee(crud.create_employee(db, employee, commerce_id=commerce_id)))
    except IntegrityError:
        return JSONResponse(content={
            "rc": -1003, "msg": 'Duplicated PIN',
        }, status_code=400)


@app.put("/employees/{employee_id}", response_model=schemas.BaseEmployeeOutput)
def update_employee(employee_id: str, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), commerce_id: HTTPBasicCredentials = Depends(get_current_commerce)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        return JSONResponse(content={
            "rc": -1001, "msg": 'Please enter a valid id',
        }, status_code=400)
    try:
        return make_json_response_with_data(crud.update_employee(db, db_employee, employee))
    except IntegrityError:
        return JSONResponse(content={
            "rc": -1003, "msg": 'Duplicated PIN',
        }, status_code=400)


@app.delete("/employees/{employee_id}", response_model=schemas.BaseOutput)
def delete_employee(employee_id: str, db: Session = Depends(get_db), commerce_id: HTTPBasicCredentials = Depends(get_current_commerce)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        return JSONResponse(content={
            "rc": -1001, "msg": 'Please enter a valid id',
        }, status_code=400)
    
    crud.delete_employee(db, db_employee)
    return make_json_response_with_data()


