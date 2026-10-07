from fastapi import FastAPI
from app.db.database import create_db

app = FastAPI()

create_db()


@app.get("/")
def health_check():
    return {"status": 200, "message": "Server is working fine"}
