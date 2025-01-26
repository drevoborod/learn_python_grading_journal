import asyncio
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from grading_journal.config import create_config
from grading_journal.database import EducationalGroups, Pupils, EducationalSubjects, group_subject_association, Grades
from grading_journal.errors import DataNotFoundError


class Repo:
    def __init__(self, engine: AsyncEngine, session: AsyncSession):
        self.engine = engine
        self.session = session


class GroupRepo(Repo):
    async def get_all(self) -> Sequence[EducationalGroups]:
        query = await self.session.scalars(select(EducationalGroups))
        return query.fetchall()

class GradesRepo(Repo):
    async def get_grades_for_pupil(self, pupil_id: int):
        query = await self.session.scalars(
            select(Grades)
            .filter_by(pupil_id=pupil_id)
            .join_from(Grades, EducationalSubjects)
            .join_from(Grades, Pupils)
        )
        return query.fetchall()

class PupilsRepo(Repo):
    async def get_for_group(self, group_id) -> Sequence[Pupils]:
        query = await self.session.scalars(select(Pupils).filter_by(educational_group_id=group_id))
        return query.fetchall()


class SubjectsRepo(Repo):
    async def get_all_subjects_for_group(self, group_id: int) -> Sequence[EducationalSubjects]:
        query = await self.session.scalars(
            select(EducationalSubjects)
            .join_from(EducationalSubjects, group_subject_association)
            .filter_by(educational_group_id=group_id)
        )
        return query.fetchall()


async def main():
    config = create_config()
    engine = create_async_engine(
        f"{config.db_driver_for_alchemy}://{config.db_user}:{config.db_password}@"
        f"{config.db_address}:{config.db_port}/{config.db_name}",
        echo=True,
    )
    session_fabric = async_sessionmaker(bind=engine)
    async with session_fabric() as session:
        g_repo = GroupRepo(engine, session)
        groups = await g_repo.get_all()
        pupil_repo = PupilsRepo(engine, session)
        pupils = await pupil_repo.get_for_group(1)
        s_repo = SubjectsRepo(engine, session)
        g_subject = await s_repo.get_all_subjects_for_group(2)
        grades_repo = GradesRepo(engine, session)
        grades = await grades_repo.get_grades_for_pupil(1)
    print([g.name for g in groups])
    print([p.last_name for p in pupils])
    print([s.name for s in g_subject])
    print([(grade.value, grade.educational_subject.name) for grade in grades])




if __name__ == "__main__":
    asyncio.run(main())




