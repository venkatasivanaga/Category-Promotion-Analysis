from uuid import uuid4
from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Run
from app.schemas.run import RunOut
from app.services.ingest import ensure_upload_dir, load_csv_from_path

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


@router.post("/{run_id}/upload", response_model=RunOut)
def upload_csv(
    run_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    upload_dir = ensure_upload_dir("uploads")
    out_path = Path(upload_dir) / f"{run_id}.csv"

    with out_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # Validate by trying to load/parse
    try:
        load_csv_from_path(str(out_path))
    except Exception as e:
        try:
            out_path.unlink(missing_ok=True)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=str(e))

    run.file_path = str(out_path)
    run.original_filename = file.filename
    run.status = "uploaded"
    db.add(run)
    db.commit()
    db.refresh(run)
    return run