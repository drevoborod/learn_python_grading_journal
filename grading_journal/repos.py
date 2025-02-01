import asyncio
from typing import Sequence, Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from grading_journal.config import create_config
from grading_journal.database import EducationalGroups, Pupils, EducationalSubjects, group_subject_association, Grades


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _insert(self, data: DeclarativeBase) -> None:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)


class GroupRepo(Repo):
    async def get_all(self) -> Sequence[EducationalGroups]:
        query = await self.session.scalars(select(EducationalGroups))
        return query.fetchall()

class GradesRepo(Repo):
    async def get_for_pupil(self, pupil_id: int) -> Sequence[Grades]:
        query = await self.session.scalars(
            select(Grades)
            .filter_by(pupil_id=pupil_id)
            .join_from(Grades, EducationalSubjects)
            .join_from(Grades, Pupils)
        )
        return query.fetchall()

#     async def get_for_group_and_subject(self, group_id: int, subject_id: int) -> Sequence[Grades]:
#         query = await self.session.scalars(
# """select eg."name", es."name", p.last_name, p.first_name, p.second_name, g.value
# from grades g
# join pupils p
# on g.pupil_id = p.id
# join educational_groups eg
# on p.educational_group_id = eg.id
# join educational_group_subjects egs
# on eg.id = egs.educational_group_id
# join educational_subjects es
# on es.id = egs.educational_subject_id
# where g.id = 1 and es.id = 2"""
#         )
#         return query.fetchall()

    async def set_for_pupil_and_subject(self, pupil_id: int, subject_id: int, value: Literal[1, 2, 3, 4, 5]) -> Grades:
        new_grade = Grades(educational_subject_id=subject_id, pupil_id=pupil_id, value=value)
        await self._insert(new_grade)
        return new_grade

class PupilsRepo(Repo):
    async def get_for_group(self, group_id) -> Sequence[Pupils]:
        query = await self.session.scalars(select(Pupils).filter_by(educational_group_id=group_id))
        return query.fetchall()


class SubjectsRepo(Repo):
    async def get_for_group(self, group_id: int) -> Sequence[EducationalSubjects]:
        query = await self.session.scalars(
            select(EducationalSubjects)
            .join_from(EducationalSubjects, group_subject_association)
            .filter_by(educational_group_id=group_id)
        )
        return query.fetchall()


async def debug_run():
    config = create_config()
    engine = create_async_engine(
        f"{config.db_driver_for_alchemy}://{config.db_user}:{config.db_password}@"
        f"{config.db_address}:{config.db_port}/{config.db_name}",
        echo=True,
    )
    session_fabric = async_sessionmaker(bind=engine)
    async with session_fabric() as session:
        g_repo = GroupRepo(session)
        groups = await g_repo.get_all()
        pupil_repo = PupilsRepo(session)
        pupils = await pupil_repo.get_for_group(1)
        s_repo = SubjectsRepo(session)
        g_subject = await s_repo.get_for_group(2)
    async with session_fabric() as session:
        grades_repo = GradesRepo(session)
        # result = await grades_repo.set_for_pupil_and_subject(1, 4, 3)
        grades = await grades_repo.get_for_pupil(1)
        # group_subject = await grades_repo.get_for_group_and_subject(group_id=1, subject_id=4)
    # print([x for x in group_subject])
    # print(result)
    print([g.name for g in groups])
    print([p.last_name for p in pupils])
    print([s.name for s in g_subject])
    print([(grade.value, grade.educational_subject.name, grade.pupil.first_name, grade.pupil.last_name) for grade in grades])




if __name__ == "__main__":
    asyncio.run(debug_run())




