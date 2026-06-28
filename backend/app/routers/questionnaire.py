from sqlalchemy.orm import Session, joinedload
from app.db.database import get_db
from app.core import oauth2
from app.db import models
from app.schemas import ModelInput, ModelResponse
from typing import List, Optional
from fastapi import HTTPException, Depends, APIRouter
import requests
from sqlalchemy.orm import Session

def predict_application(application_id: int, db: Session):
    application = (
        db.query(models.CreditApplication)
        .filter(models.CreditApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Credit application record not found")

    payload = {
        "loan_amnt": application.loan_amnt,
        "annual_inc": application.annual_inc,
        "dti": application.dti,
        "installment": application.installment,
        "fico_score": application.fico_score,
        "tot_cur_bal": application.tot_cur_bal,
        "revol_util": application.revol_util,
        "emp_length": application.emp_length,
        "home_ownership": application.home_ownership,
        "inq_last_6mths": application.inq_last_6mths,
        "delinq_2yrs": application.delinq_2yrs,
        "pct_tl_nvr_dlq": application.pct_tl_nvr_dlq,
        "open_acc": application.open_acc,
        "total_acc": application.total_acc,
        "bc_util": application.bc_util,
        "avg_cur_bal": application.avg_cur_bal,
        "acc_open_past_24mths": application.acc_open_past_24mths,
        "grade": application.grade,
        "sub_grade": application.sub_grade,
        "purpose": application.purpose,
        "verification_status": application.verification_status,
        "credit_history_years": application.credit_history_years,
    }

    response = requests.post(
        "http://127.0.0.1:8001/predict",
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


router = APIRouter(
    tags=["Upload"]
)

@router.post("/applications/{application_id}/predict", response_model=ModelResponse)
def predict(application_id: int, db: Session = Depends(get_db)):
    return predict_application(application_id, db)