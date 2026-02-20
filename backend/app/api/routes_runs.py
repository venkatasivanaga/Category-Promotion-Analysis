from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Run
from app.schemas.run import RunOut

router = APIRouter(prefix="/runs", tags=["runs"])

@router.post("", response_model=RunOut)
def create_run(db: Session = Depends(get_db)):
    run_id = str(uuid4())
    run = Run(id=run_id, status="created")
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

@router.get("", response_model=list[RunOut])
def list_runs(db: Session = Depends(get_db)):
    return db.query(Run).order_by(Run.created_at.desc()).limit(50).all()

@router.get("/{run_id}", response_model=RunOut)
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run