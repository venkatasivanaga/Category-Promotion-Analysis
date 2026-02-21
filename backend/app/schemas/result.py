from pydantic import BaseModel

class RunResultsOut(BaseModel):
    run_id: str
    summary: dict