from pydantic import BaseModel
from datetime import datetime, timezone
from pydantic.datetime_parse import parse_datetime


class utc_datetime(datetime):

	@classmethod
	def __get_validators__(self):
		yield parse_datetime  # default pydantic behavior
		yield self.ensure_tzinfo

	@classmethod
	def ensure_tzinfo(self, v: datetime):
		# if TZ isn't provided, we assume UTC, but you can do w/e you need
		if v.tzinfo is None:
			return v.replace(tzinfo=timezone.utc)
		# else we convert to utc
		return v.astimezone(timezone.utc)

	@staticmethod
	def to_str(dt: datetime) -> str:
		return dt.isoformat()  # replace with w/e format you want


class PlayerBase(BaseModel):
	steam_id: str

	class Config:
		orm_mode = True


class PlayerInput(PlayerBase):
	pass


class Player(PlayerBase):
	pings: int


class Players(BaseModel):
	players: list[str]


class MissionBase(BaseModel):
	file_name: str

	class Config:
		orm_mode = True


class MissionCreate(MissionBase):
	pass


class MissionCreateResponse(MissionBase):
	id: int
	start_time: utc_datetime


class Mission(MissionBase):
	id: int
	start_time: utc_datetime
	end_time: utc_datetime | None
	pings: int
	players: list[Player]
