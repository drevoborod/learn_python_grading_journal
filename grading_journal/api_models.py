from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class EducationalGroup(BaseModel):
    id: int
    name: str


class EducationalSubject(BaseModel):
    id: int
    name: str


class Pupil(BaseModel, from_attributes=True):
    id: int
    first_name: str
    last_name: str
    second_name: str | None
    birth_date: datetime | None
    social_ensurance_id: str | None
    educational_group_id: int


class SetGrade(BaseModel):
    value: Literal[1, 2, 3, 4, 5]
