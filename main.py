from fastapi import FastAPI
import subprocess
import pandas as pd

app = FastAPI()

@app.get("/run-optimizer")
def run_optimizer():
    # This runs your logic script when the URL is visited
    subprocess.run(["python", "recommendation_engine.py"])
    return {"status": "Success", "message": "Recommendations generated!"}

@app.get("/get-results")
def get_results():
    # This sends the data from the CSV to the frontend
    df = pd.read_csv("submission.csv")
    return df.to_dict(orient="records")