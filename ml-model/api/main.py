from fastapi import FastAPI
from schemas import LoanApplication
from predictor import predict

app = FastAPI(
    title="WiseLenderAI"
)

@app.get("/")
def root():
    return {
        "status": "running"
    }

@app.post("/predict")
def predict_loan(
    application: LoanApplication
):

    return predict(
        application.dict()
    )