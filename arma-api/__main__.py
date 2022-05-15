from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
	"""Root request"""
	return {"message": "Hello World"}


@app.post("/test")
async def test(users: list[str]):
	print(users)
	return {"response": "success"}


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app)
