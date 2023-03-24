from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

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

	id: Mapped[int] = mapped_column(primary_key=True)
	file_name: Mapped[str] = mapped_column()
	start_time: Mapped[datetime] = mapped_column(default=utctime)
	end_time: Mapped[datetime] = mapped_column(
		default=utctime, onupdate=utctime
	)
	pings: Mapped[int] = mapped_column(server_default="0")

	players: Mapped[list] = relationship(
		"Player",
		#cascade="save-update, merge, delete, delete-orphan",
		back_populates="mission",
		lazy="immediate",
		cascade="all, delete",
		passive_deletes=True,
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

	id: Mapped[int] = mapped_column(primary_key=True)
	mission_id: Mapped[int] = mapped_column(
		ForeignKey("missions.id", ondelete="CASCADE")
	)
	steam_id: Mapped[str] = mapped_column()
	pings: Mapped[int] = mapped_column(server_default="1")

	mission: Mapped[Mission] = relationship(
		"Mission",
		back_populates="players",
		uselist=False,
	)

	__mapper_args__ = {"eager_defaults": True}
