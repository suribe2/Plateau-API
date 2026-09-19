from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base, engine

class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(Date)
    exercise_title = Column(String)
    set_type = Column(String)
    weight_lbs = Column(Float)
    reps = Column(Integer)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Table created (or already exists).")
