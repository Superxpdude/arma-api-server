from pydantic import BaseModel
from datetime import datetime


class PlayerBase(BaseModel):
	steam_id: str

	class Config:
		orm_mode = True


class PlayerInput(PlayerBase):
	pass


class Player(PlayerBase):
	pings: int


class MissionBase(BaseModel):
	file_name: str

	class Config:
		orm_mode = True


class MissionCreate(MissionBase):
	pass


class MissionCreateResponse(MissionBase):
	id: int
	start_time: datetime


class Mission(MissionBase):
	id: int
	start_time: datetime
	end_time: datetime | None
	pings: int
	players: list[Player]
