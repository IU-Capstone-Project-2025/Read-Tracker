from sqlalchemy import create_engine
from src.database.models import Base
import os

# postgresql://postgres:password@database:5432/reader_library_db

pg_user = os.getenv("POSTGRES_USER")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DB")

engine = create_engine(
    url=f"postgresql://{pg_user}:{pg_password}@database:5432/{pg_db}",
    echo=False
)

Base.metadata.create_all(engine)
