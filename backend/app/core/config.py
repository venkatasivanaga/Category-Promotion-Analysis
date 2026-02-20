from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "Category Promotion Analysis API"
    cors_origins: list[str] = ["*"]  # dev default

def _parse_origins(value: str | None) -> list[str]:
    """
    Accepts:
      - "*"  -> allow all
      - "http://a.com,http://b.com" -> list
    """
    if not value:
        return ["*"]
    v = value.strip()
    if v == "*":
        return ["*"]
    return [x.strip() for x in v.split(",") if x.strip()]

settings = Settings(cors_origins=_parse_origins(os.getenv("CORS_ORIGINS")))