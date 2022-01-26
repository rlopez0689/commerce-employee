from datetime import datetime
from typing import List, Optional
from xmlrpc.client import boolean

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    pin: str


class EmployeeCreate(EmployeeBase):
    name: str
    last_name: str


class EmployeeUpdate(EmployeeBase):
    name: str
    last_name: str
    active: boolean


class Employee(EmployeeBase):
    id: str 
    full_name: str
    created_on: datetime
    active: boolean

    class Config:
        orm_mode = True

class BaseEmployeesOutput(BaseModel):
    data: List[Employee]
    rc: int
    msg: str

class BaseEmployeeOutput(BaseModel):
    data: Employee
    rc: int
    msg: str

class BaseOutput(BaseModel):
    data: List
    rc: int
    msg: str
