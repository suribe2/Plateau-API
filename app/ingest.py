import pandas as pd
from app.database import SessionLocal
from app.models import WorkoutSet

df = pd.read_csv("data/synthetic_workout_data.csv")
df["start_time"] = pd.to_datetime(df["start_time"], format="%d %b %Y, %H:%M")

session = SessionLocal()

for _, row in df.iterrows():
    workout_set = WorkoutSet(
        title=row["title"],
        date=row["start_time"].date(),
        exercise_title=row["exercise_title"],
        set_type=row["set_type"],
        weight_lbs=row["weight_lbs"],
        reps=row["reps"],
    )
    session.add(workout_set)

session.commit()
session.close()
print(f"Ingested {len(df)} rows.")