from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Category Promotion Analysis API"

settings = Settings()