from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

# ----------------------------- Measurment
class MeasurmentBase(BaseModel):
    valve_number: int
    start_date: datetime
    end_date: datetime
    responsible: str
    department: str
    dripper_volume: float
    dripper_ec: float
    dripper_ph: float
    drain_volume: float
    drain_ec: float
    drain_ph: float
    mat_ec: float
    mat_ph: float
    
class MeasurmentCreate(MeasurmentBase):
    pass

class Measurment(MeasurmentBase):
    id: int
    class Config:
        orm_mode = True
# ----------------------------- Note
# class NoteBase(BaseModel):
#     text: str
# class NoteCreate(NoteBase):
#     pass
# class Note(NoteBase):
#     id: int
#     owner_id: int
#     class Config:
#         orm_mode = True
# ----------------------------- Title
# class TitleBase(BaseModel):
#     name: str
#     is_important: Union[bool, None] = None
#     parent_id: Union[int, None] = None
# class TitleCreate(TitleBase):
#     pass
# class TitleChild(TitleBase):
#     id: int
#     owner_id: int
#     class Config:
#         orm_mode = True
# class Title(TitleBase):
#     id: int
#     owner_id: int

#     notes: List[Note] = []
#     parent_title: Union[TitleChild, None] = None
#     # children_title: List[Union[TitleBase, None]] = None
#     class Config:
#         orm_mode = True

# ----------------------------- User

class UserBase(BaseModel):
    email: str
class UserCreate(UserBase):
    password: str
class User(UserBase):
    id: int
    is_active: bool
    # titles: List[Title] = []

    class Config:
        orm_mode = True
# ----------------------------- Token

class Token(BaseModel):
    access_token: str
    token_type: str