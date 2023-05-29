from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base

"""
Список таблиц для приложения для сохранения научных данных
# / in ideal world /
- Department
- Measurment
- Type
- Action
- Parameter
- Valve
- MeasurmentElement

Measurment owns many Department
Parameter owns many Type
Parameter owns many Action
MeasurmentElement owns many Measurment
MeasurmentElement owns many Parameter

"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    # meta
    # titles = relationship("Title", back_populates="user_owner") # child link

class Measurment(Base): # crude implementation # TODO
    __tablename__ = "measurments"

    id = Column(Integer, primary_key=True, index=True)
    valve_number = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    responsible = Column(String(100))
    department = Column(String(100))
    # 
    dripper_volume = Column(Float)
    dripper_ec = Column(Float)
    dripper_ph = Column(Float)
    drain_volume = Column(Float)
    drain_ec = Column(Float)
    drain_ph = Column(Float)
    mat_ec = Column(Float)
    mat_ph = Column(Float)

# ///////////// for ideal world

# class Department(Base):
#     __tablename__ = "department"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100))

# class Measurment(Base):
#     __tablename__ = "measurment"

#     id = Column(Integer, primary_key=True, index=True)
#     start_date = Column(DateTime)
#     end_date = Column(DateTime)
#     department_id = Column(Integer, ForeignKey('department.id'))

# class Type(Base):
#     __tablename__ = "type"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100))

# class Action(Base):
#     __tablename__ = "action"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100))

# class Parameter(Base):
#     __tablename__ = "parameter"

#     id = Column(Integer, primary_key=True, index=True)
#     type_id = Column(Integer, ForeignKey('type.id'))
#     action_id = Column(Integer, ForeignKey("action.id"))

# class Valve(Base):
#     __tablename__ = "valve"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100))

# class MeasurmentElement(Base):
#     __tablename__ = "measurment_element"

#     id = Column(Integer, primary_key=True, index=True)
#     measurment_id = Column(Integer, ForeignKey('measurment.id'))
#     valve_id = Column(Integer, ForeignKey("valve.id"))
#     parameter_id = Column(Integer, ForeignKey("parameter.id"))
#     value = Column(Float)
