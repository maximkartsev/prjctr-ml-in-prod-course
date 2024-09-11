import uvicorn
from fastapi import FastAPI, HTTPException
from api.model import RegressionModel
from api.prediction import predict_logic
from api.shard_and_upload import shard_and_upload_logic
from api.train_model import train_logic

app = FastAPI()

# Create a route for prediction
@app.get("/predict")
def predict(text: str):
    try:
        return predict_logic(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a route for sharding and uploading data to MinIO
@app.get("/shard-and-upload")
def shard_and_upload(csv_file_path: str):
    try:
        shard_and_upload_logic(csv_file_path)
        return {"message": "Sharding and uploading to MinIO completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a route for training the model
@app.get("/train")
def train_model():
    try:
        train_logic()
        return {"message": "Model training completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
