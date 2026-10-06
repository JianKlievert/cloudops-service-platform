from sqlalchemy import select
from datetime import datetime, timezone
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Job
from app.schemas import JobCreate

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"status": "Database connection successful"}


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    result = db.execute(select(Job))
    jobs = result.scalars().all()
    return jobs


@app.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(
        type=job.type,
        input=job.input,
        status="pending",
        created_at=datetime.now(timezone.utc),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
