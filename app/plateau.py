import pandas as pd
from app.database import engine

df = pd.read_sql("SELECT * FROM workout_sets", engine)

df["date"] = pd.to_datetime(df["date"])
df["week"] = df["date"].dt.isocalendar().week

df = df[(df["exercise_title"].isin(["Smith Machine Incline Bench", "Leg Press"])) &
        (df["set_type"] != "warmup") &
        (df["reps"] >= 5)
]

print(df["exercise_title"].unique())
