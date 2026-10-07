from fastapi import FastAPI
from app.db.database import create_db
from app.routers.auth_routers import router as auth_routers

app = FastAPI()

create_db()


@app.get("/")
def health_check():
    return {"status": 200, "message": "Server is working fine"}


app.include_router(auth_routers)
