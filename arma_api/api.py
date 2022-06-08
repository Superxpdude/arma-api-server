from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from datetime import datetime, timezone, timedelta

from .db import models

from . import schemas
from .db.config import engine, async_session, Base

app = FastAPI()

active_players: list[models.Player] = []
last_update_time: datetime = None


@app.on_event("startup")
async def startup():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


@app.middleware("http")
async def auth_check(request: Request, call_next):
	response = await call_next(request)
	print(response.headers)
	return response


@app.post(
	"/mission", response_model=schemas.MissionCreateResponse, status_code=201
)
async def create_mission(mission: schemas.MissionCreate):
	async with async_session() as session:
		db: Session = session
		dbMission = models.Mission(file_name=mission.file_name)
		async with db.begin():
			db.add(dbMission)
		return dbMission


@app.patch("/mission/{mission_id}", response_model=schemas.Mission)
async def update_mission(mission_id: int, playerIDs: list[str]):
	async with async_session() as session:
		session: Session

		# Access this global variable to set our list of currently connected players
		global active_players
		global last_update_time

		async with session.begin():

			dbMission: models.Mission = await session.get(
				models.Mission, mission_id
			)
			if dbMission is None:
				raise HTTPException(
					status_code=404,
					detail=f"Mission with ID: {mission_id} could not be found"
				)

			# Increment existing player counts
			for player in dbMission.players:
				player: models.Player
				if player.steam_id in playerIDs:
					player.pings += 1
					playerIDs.remove(player.steam_id)

			# Make new player objects for remaining steam IDs
			for playerID in playerIDs:
				player = models.Player(steam_id=playerID)
				dbMission.players.append(player)

			# Update our active players list
			active_players = []
			for player in dbMission.players:
				player: models.Player
				active_players.append(player.steam_id)

			# Increment our last updated time
			last_update_time = datetime.now(tz=timezone.utc)

			# Increment mission ping counter
			dbMission.pings += 1

		return dbMission


@app.get("/missions", response_model=list[schemas.Mission])
async def list_missions():
	async with async_session() as session:
		session: Session

		dbResult = await session.execute(select(models.Mission))

		missions = dbResult.scalars().all()

		return missions


@app.get("/mission/{mission_id}", response_model=schemas.Mission)
async def get_mission(mission_id: int):
	async with async_session() as session:
		session: Session

		dbMission: models.Mission = await session.get(
			models.Mission, mission_id
		)

		if dbMission is None:
			raise HTTPException(
				status_code=404,
				detail=f"Mission with ID: {mission_id} could not be found"
			)

		return dbMission


@app.get("/players")
async def get_players():
	global last_update_time
	global active_players

	# If it has been more than two minutes since the last update, clear our player list before returning
	if (
		(last_update_time is not None) and (
			(last_update_time + timedelta(minutes=2)) <
			datetime.now(tz=timezone.utc)
		)
	):
		active_players = []

	return active_players


@app.delete("/mission/{mission_id}")
async def delete_mission(mission_id: int):
	async with async_session() as session:
		session: Session

		async with session.begin():
			dbMission: models.Mission = await session.get(
				models.Mission, mission_id
			)
			if dbMission is None:
				raise HTTPException(
					status_code=404,
					detail=f"Mission with ID: {mission_id} could not be found"
				)

			await session.delete(dbMission)

		return
