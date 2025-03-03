from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from grading_journal.api_models import EducationalGroup, EducationalSubject, Pupil, SetGrade, Grade
from grading_journal.config import create_config
from grading_journal.repos import GroupRepo, SubjectsRepo, PupilsRepo, GradesRepo


router = APIRouter()


async def database_session():
    config = create_config()
    engine = create_async_engine(
        f"{config.db_driver_for_alchemy}://{config.db_user}:{config.db_password}@"
        f"{config.db_address}:{config.db_port}/{config.db_name}",
        echo=True,
    )
    yield async_sessionmaker(bind=engine)


@router.get(
    "/groups/",
    summary="Get educational groups list"
)
async def groups(
        db_session_fabric: Annotated[async_sessionmaker, Depends(database_session)]
) -> list[EducationalGroup]:
    async with db_session_fabric() as session:
        g_repo = GroupRepo(session)
        educational_groups = await g_repo.get_all()
    return [EducationalGroup(id=group.id, name=group.name) for group in educational_groups]


@router.get(
    "/groups/{group_id}/subjects/",
    summary="Get all subjects within group."
)
async def group_subjects(
        db_session_fabric: Annotated[async_sessionmaker, Depends(database_session)],
        group_id: int,
) -> list[EducationalSubject]:
    async with db_session_fabric() as session:
        g_repo = SubjectsRepo(session)
        educational_subjects = await g_repo.get_for_group(group_id)
    return [EducationalSubject(id=subject.id, name=subject.name) for subject in educational_subjects]


@router.get(
    "/groups/{group_id}/pupils/",
    summary="Get all pupils within group."
)
async def group_pupils(
        db_session_fabric: Annotated[async_sessionmaker, Depends(database_session)],
        group_id: int,
) -> list[Pupil]:
    async with db_session_fabric() as session:
        g_repo = PupilsRepo(session)
        pupils = await g_repo.get_for_group(group_id)
    return [Pupil.model_validate(pupil) for pupil in pupils]


@router.get(
    "/groups/{group_id}/subjects/{subject_id}/grades/",
    summary="Get all pupil's grades for specific subject within group."
)
async def group_grade(
        db_session_fabric: Annotated[async_sessionmaker, Depends(database_session)],
        group_id: int,
        subject_id: int,
) -> list[Grade]:
    async with db_session_fabric() as session:
        g_repo = GradesRepo(session)
        grades = await g_repo.get_for_group_and_subject(group_id=group_id, subject_id=subject_id)
    return [Grade.model_validate(grade) for grade in grades]

@router.post(
    "/pupils/{pupil_id}/subjects/{subject_id}/grades/",
    summary="Set grade for specific pupil and subject."
)
async def set_grade(
        db_session_fabric: Annotated[async_sessionmaker, Depends(database_session)],
        request: SetGrade,
        pupil_id: int,
        subject_id: int
):
    async with db_session_fabric() as session:
        g_repo = GradesRepo(session)
        await g_repo.set_for_pupil_and_subject(pupil_id=pupil_id, subject_id=subject_id, value=request.value)
