from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from app.db.deps import get_db
from app.db.models import Run
from app.schemas.run import RunOut
from app.services.ingest import ensure_upload_dir, load_csv_from_path

router = APIRouter(prefix="/runs", tags=["runs"])

@router.post("/{run_id}/upload", response_model=RunOut)
def upload_csv(run_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
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
        _df = load_csv_from_path(str(out_path))
    except Exception as e:
        # Remove invalid file to keep directory clean
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