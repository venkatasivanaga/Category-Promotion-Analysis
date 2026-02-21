import pytest
from sqlalchemy import create_engine

from app.db.session import Base
from app.db import models  # noqa: F401


@pytest.fixture(autouse=True)
def _set_test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )

    # IMPORTANT: reset schema every test run (since we aren't using migrations yet)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield