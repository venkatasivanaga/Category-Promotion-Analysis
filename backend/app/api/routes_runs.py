from uuid import uuid4
from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Run
from app.schemas.run import RunOut
from app.services.ingest import ensure_upload_dir, load_csv_from_path
import json
from app.db.models import RunResult
from app.services.analyze import compute_category_uplift
from app.services.ingest import load_csv_from_path
from app.schemas.result import RunResultsOut

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


@router.post("/{run_id}/analyze", response_model=RunResultsOut)
def analyze_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    if not run.file_path:
        raise HTTPException(status_code=400, detail="No uploaded CSV for this run")

    df = load_csv_from_path(run.file_path)
    summary = compute_category_uplift(df)

    existing = db.query(RunResult).filter(RunResult.run_id == run_id).first()
    payload = json.dumps(summary)

    if existing:
        existing.summary_json = payload
        db.add(existing)
    else:
        db.add(RunResult(run_id=run_id, summary_json=payload))

    run.status = "analyzed"
    db.add(run)
    db.commit()

    return {"run_id": run_id, "summary": summary}

@router.get("/{run_id}/results", response_model=RunResultsOut)
def get_results(run_id: str, db: Session = Depends(get_db)):
    rr = db.query(RunResult).filter(RunResult.run_id == run_id).first()
    if not rr:
        raise HTTPException(status_code=404, detail="Results not found")
    return {"run_id": run_id, "summary": json.loads(rr.summary_json)}