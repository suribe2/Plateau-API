import pandas as pd

# Load the raw Hevy export (one row per set)
df = pd.read_csv("synthetic_workout_data.csv")

# Keep only the two lifts we're tracking for plateau detection,
# drop warmup sets, and drop any set with fewer than 5 reps
# (5+ reps = "meaningful" working set, filters out low-rep ego singles)
df = df[
    (df["exercise_title"].isin(["Smith Machine Incline Bench", "Leg Press"])) &
    (df["set_type"] != "warmup") &
    (df["reps"] >= 5)
]

# Convert start_time from text ("27 Jul 2026, 17:00") into a real datetime
# so we can do date math (grouping by week) on it
df["start_time"] = pd.to_datetime(df["start_time"], format="%d %b %Y, %H:%M")

# Bucket each set into its ISO calendar week (Mon-Sun) for weekly grouping
df["week"] = df["start_time"].dt.isocalendar().week

#print(df[["start_time", "week"]])

# Sort so the "best" set (heaviest weight, then most reps as tiebreaker)
# comes first within each exercise+week group
df_sorted = df.sort_values(
    by=["exercise_title", "week", "weight_lbs", "reps"],
    ascending=[True, True, False, False]
)

# Take the first row of each (exercise, week) group -> that's the top set,
# since we already sorted heaviest-first
top_sets = df_sorted.groupby(["exercise_title", "week"]).first().reset_index()

# Re-sort chronologically so shift() below compares each week to the
# correct previous week within the same exercise
top_sets = top_sets.sort_values(["exercise_title", "week"])

# Pull last week's top-set weight/reps onto this week's row, per exercise,
# so we can compare week-over-week
top_sets["prev_weight"] = top_sets.groupby("exercise_title")["weight_lbs"].shift(1)
top_sets["prev_reps"] = top_sets.groupby("exercise_title")["reps"].shift(1)

# "Improved" if weight went up (regardless of reps),
# OR weight stayed the same and reps went up.
# NaN comparisons (week 1, no prior data) evaluate to False automatically.
top_sets["improved"] = (top_sets["weight_lbs"] > top_sets["prev_weight"]) | (
    (top_sets["weight_lbs"] == top_sets["prev_weight"]) & (top_sets["reps"] > top_sets["prev_reps"])
)

# Walk through each exercise's weeks in order, tracking a streak of
# consecutive no-improvement weeks. Once the streak hits 3, flag plateau.
plateau_flags = []

for exercise in top_sets["exercise_title"].unique():
    subset = top_sets[top_sets["exercise_title"] == exercise]
    streak = 0
    for improved_value in subset["improved"]:
        if improved_value:
            streak = 0          # reset on any improvement
        else:
            streak += 1         # no improvement -> extend the streak

        plateau_flags.append(streak >= 3)

top_sets["plateau"] = plateau_flags

print(top_sets[["exercise_title", "week", "improved", "plateau"]])