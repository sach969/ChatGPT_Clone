from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
DATABASE_URL = os.getenv("database_url")

engine = create_engine(DATABASE_URL,echo=True)
sessionlocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

# Dependency function for FastAPI to get DB session
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
