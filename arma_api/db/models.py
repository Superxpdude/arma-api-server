from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime, timezone

from .config import Base


def utctime():
	"""Small helper function to return a timezone-aware UTC time object"""
	return datetime.now(tz=timezone.utc)


class Mission(Base):
	"""Database class for mission information.

	Parameters
	----------
	id : int
		Unique ID. Automatically set by database.
	file_name : str
		Name of the mission.
	start_time : int
		Unix timestamp of the mission start time.
	end_time : int
		Unix timestamp of the mission end time.
	pings : int
		Number of times the current players were grabbed during the mission.
	"""
	__tablename__ = "missions"

	id = Column(Integer, primary_key=True)
	file_name = Column(String)
	start_time = Column(DateTime(timezone=True), default=utctime)
	end_time = Column(
		DateTime(timezone=True), default=utctime, onupdate=utctime
	)
	pings = Column(Integer, server_default="0")

	players: list = relationship(
		"Player",
		#cascade="save-update, merge, delete, delete-orphan",
		back_populates="mission",
		lazy="immediate"
	)

	__mapper_args__ = {"eager_defaults": True}


class Player(Base):
	"""Database class for mission information.

	Parameters
	----------
	mission_id : int
		Foreign key ID of the mission.
	steam_id : str
		Steam64ID of the user in string form.
	pings : int
		Number of times the player was seen during the mission.
	"""
	__tablename__ = "players"

	id = Column(Integer, primary_key=True)
	mission_id = Column(Integer, ForeignKey("missions.id", ondelete="CASCADE"))
	steam_id = Column(String)
	pings = Column(Integer, server_default="1")

	mission: Mission = relationship(
		"Mission",
		back_populates="players",
		uselist=False,
	)

	__mapper_args__ = {"eager_defaults": True}
