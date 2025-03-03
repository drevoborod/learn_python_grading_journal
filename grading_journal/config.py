import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    db_user: str
    db_password: str
    db_name: str
    db_address: str
    db_port: str
    db_driver_for_alchemy: str


def create_config():
    load_dotenv()
    return Config(
        db_user=os.environ["GRADING_JOURNAL_DATABASE_USER"],
        db_password=os.environ["GRADING_JOURNAL_DATABASE_PASSWORD"],
        db_name=os.environ["GRADING_JOURNAL_DATABASE_NAME"],
        db_address=os.environ["GRADING_JOURNAL_DATABASE_ADDRESS"],
        db_port=os.environ["GRADING_JOURNAL_DATABASE_PORT"],
        db_driver_for_alchemy="postgresql+asyncpg"
    )