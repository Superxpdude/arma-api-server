from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import datetime

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./data/arma_api.sqlite3"

engine = create_async_engine(
	SQLALCHEMY_DATABASE_URL,
	future=True,
	connect_args={"check_same_thread": False},
)

async_session = sessionmaker(
	engine,
	expire_on_commit=False,
	class_=AsyncSession,
)


class Base(DeclarativeBase):
	type_annotation_map = {datetime.datetime: TIMESTAMP(timezone=True)}
