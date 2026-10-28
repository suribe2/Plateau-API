from sqlalchemy import Column, Integer, String, Float, Date, Text
from pgvector.sqlalchemy import Vector
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

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    content = Column(Text)
    source = Column(String)
    embedding = Column(Vector(1536))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Table created (or already exists).")