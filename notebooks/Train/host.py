from fastapi import FastAPI
from train import forecast
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the water level forecasting API"}

@app.get("/forecast")
def get_forecast():
    final_result = forecast()
    return final_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
