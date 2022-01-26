from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import EmailType

from .database import Base
import uuid
import datetime


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, default=lambda: str(uuid.uuid4()))
    name = Column(String(40), index=True)
    last_name = Column(String(40), index=True)
    pin = Column(String(6), index=True)
    commerce_id = Column(Integer, ForeignKey("commerce.id"))
    commerce = relationship("Commerce") 
    created_on = Column(DateTime, default=datetime.datetime.now)
    active = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint('pin', 'commerce_id', name='_pin_commerce_uc'),)

    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.last_name}"

class Commerce(Base):
    __tablename__ = "commerce"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), index=True)
    active = Column(Boolean, default=True)
    email = Column(EmailType(50))
    phone = Column(String(15), unique=True, index=True)
    api_key = Column(String, default=lambda: str(uuid.uuid4()))
    created_on = Column(DateTime, default=datetime.datetime.now) 