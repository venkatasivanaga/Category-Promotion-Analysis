from pydantic import BaseModel
from datetime import datetime

class RunOut(BaseModel):
    id: str
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    file_path: str | None = None
    original_filename: str | None = None