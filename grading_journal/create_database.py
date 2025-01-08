from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass


class Pupil(Base):
    __tablename__ = "pupils"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    second_name: Mapped[Optional[str]]
    birth_date: Mapped[Optional[datetime]]
    social_ensurance_id: Mapped[Optional[str]]


class EducationalGroup(Base):
    __tablename__ = "educational_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class EducationalSubject(Base):
    __tablename__ = "educational_subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]


class PupilGroup(Base):
    __tablename__ = "pupil_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    pupil_id = mapped_column(ForeignKey(Pupil.id))
    group_id = mapped_column(ForeignKey(EducationalGroup.id))


class PupilSubjectGrade(Base):
    __tablename__ = "pupil_subject_grade"

    id: Mapped[int] = mapped_column(primary_key=True)
    pupil_id = mapped_column(ForeignKey(Pupil.id))
    subject_id = mapped_column(ForeignKey(EducationalSubject.id))
    grade_id = mapped_column(ForeignKey(Grade.id))


def create_tables(engine):
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    engine = create_engine("postgresql+psycopg2://grading_journal:postgres@localhost:15432/grading_journal", echo=True)
    create_tables(engine)
