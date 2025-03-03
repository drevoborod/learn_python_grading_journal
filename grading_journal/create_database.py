import asyncio
import time

from asyncpg import CannotConnectNowError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from grading_journal.database import Base
from grading_journal.config import create_config


async def create_tables(engine: AsyncEngine, base_class: type[DeclarativeBase]):
    async with engine.begin() as connection:
        await connection.run_sync(base_class.metadata.create_all)


if __name__ == "__main__":
    config = create_config()
    engine = create_async_engine(
        f"{config.db_driver_for_alchemy}://{config.db_user}:{config.db_password}@"
        f"{config.db_address}:{config.db_port}/{config.db_name}",
        echo=True,
    )
    asyncio.run(create_tables(engine, Base))
