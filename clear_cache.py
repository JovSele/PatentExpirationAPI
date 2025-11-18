from app.database import engine, Base
from app.models import PatentCache
from sqlalchemy.orm import Session

with Session(engine) as session:
    session.query(PatentCache).delete()
    session.commit()
    print("✅ Cache cleared!")