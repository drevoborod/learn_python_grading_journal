from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Table, Column, DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Pupils(Base):
    __tablename__ = "pupils"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    second_name: Mapped[Optional[str]]
    birth_date: Mapped[Optional[datetime]]
    social_ensurance_id: Mapped[Optional[str]]
    educational_group_id = mapped_column(ForeignKey("educational_groups.id"))

    grades: Mapped["Grades"] = relationship()
    educational_group: Mapped["EducationalGroups"] = relationship(back_populates="pupils")


group_subject_association = Table(
    "educational_group_subjects",
    Base.metadata,
    Column("educational_subject_id", ForeignKey("educational_subjects.id")),
    Column("educational_group_id", ForeignKey("educational_groups.id")),
)


class EducationalGroups(Base):
    __tablename__ = "educational_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    pupils: Mapped[Pupils] = relationship(back_populates="educational_group")
    educational_subjects: Mapped["EducationalSubjects"] = relationship(
        back_populates="educational_groups", secondary=group_subject_association)


class EducationalSubjects(Base):
    __tablename__ = "educational_subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    educational_groups: Mapped[EducationalGroups] = relationship(
        back_populates="educational_subjects", secondary=group_subject_association
    )


class Grades(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    educational_subject_id = mapped_column(ForeignKey(EducationalSubjects.id))
    pupil_id = mapped_column(ForeignKey(Pupils.id))
    value: Mapped[int]
    educational_group_id = mapped_column(ForeignKey(EducationalGroups.id))
    created_at = Column(DateTime, nullable=False, server_default=text("NOW()"))

    pupil: Mapped[Pupils] = relationship(lazy="selectin")
    educational_subject: Mapped[EducationalSubjects] = relationship(lazy="selectin")
    group: Mapped[EducationalGroups] = relationship(lazy="selectin")
