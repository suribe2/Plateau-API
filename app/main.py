import json
from fastapi import FastAPI
from app.plateau import detect_plateaus

app = FastAPI(title="Plateau Tracker")

@app.get("/plateaus")
def get_plateaus():
    results = detect_plateaus()[["exercise_title", "week", "weight_lbs", "reps", "improved", "plateau"]]
    return json.loads(results.to_json(orient="records"))

