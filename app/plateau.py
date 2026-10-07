import pandas as pd
from app.database import engine


def detect_plateaus():
    df = pd.read_sql("SELECT * FROM workout_sets", engine)

    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week

    # 1. Filter first: only the two lifts, no warmups, 5+ reps
    df = df[(df["exercise_title"].isin(["Smith Machine Incline Bench", "Leg Press"])) &
            (df["set_type"] != "warmup") &
            (df["reps"] >= 5)
    ]

    # 2. Top set per exercise per week (heaviest weight, reps as tiebreaker)
    df_sorted = df.sort_values(
        by=["exercise_title", "week", "weight_lbs", "reps"],
        ascending=[True, True, False, False]
    )
    top_sets = df_sorted.groupby(["exercise_title", "week"]).first().reset_index()

    # 3. Pull the previous week's top set onto each row, per exercise
    top_sets = top_sets.sort_values(["exercise_title", "week"])
    top_sets["prev_weight"] = top_sets.groupby("exercise_title")["weight_lbs"].shift(1)
    top_sets["prev_reps"] = top_sets.groupby("exercise_title")["reps"].shift(1)

    # 4. Improved = heavier weight, or same weight with more reps
    top_sets["improved"] = (top_sets["weight_lbs"] > top_sets["prev_weight"]) | (
        (top_sets["weight_lbs"] == top_sets["prev_weight"]) & (top_sets["reps"] > top_sets["prev_reps"])
    )

    # 5. Streak counter: 3 weeks in a row with no improvement = plateau
    plateau_flags = []
    for exercise in top_sets["exercise_title"].unique():
        subset = top_sets[top_sets["exercise_title"] == exercise]
        streak = 0
        for improved_value in subset["improved"]:
            if improved_value:
                streak = 0
            else:
                streak += 1
            plateau_flags.append(streak >= 3)

    top_sets["plateau"] = plateau_flags

    return top_sets


if __name__ == "__main__":
    print(detect_plateaus()[["exercise_title", "week", "improved", "plateau"]])
