from sqlalchemy.orm import Session, joinedload
from app.db.database import get_db
from app.core import oauth2
from app.db import models
from app.schemas import ModelInput, ModelResponse, CreditApplicationOut
from typing import List, Optional
from fastapi import HTTPException, Depends, APIRouter
import requests

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.post("/", response_model=CreditApplicationOut, status_code=201)
def create_application(payload: ModelInput, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_app = models.CreditApplication(
        user_id=current_user.id,
        **payload.model_dump()
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.get("/", response_model=List[CreditApplicationOut])
def get_applications(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    applications = db.query(models.CreditApplication).filter(models.CreditApplication.user_id == current_user.id).all()
    return applications

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
        "installment": application.installment,
        "dti": application.dti,
        "tot_cur_bal": application.tot_cur_bal,
        "avg_cur_bal": application.avg_cur_bal,
        "open_acc": application.open_acc,
        "total_acc": application.total_acc,
        "emp_length": application.emp_length,
        "revol_util": application.revol_util,
        "bc_util": application.bc_util,
        "home_ownership": application.home_ownership,
        "purpose": application.purpose,
        "verification_status": application.verification_status,
        "FLAG_MOBIL": application.FLAG_MOBIL,
        "FLAG_PHONE": application.FLAG_PHONE,
        "FLAG_WORK_PHONE": application.FLAG_WORK_PHONE,
        "FLAG_CONT_MOBILE": application.FLAG_CONT_MOBILE,
        "FLAG_EMAIL": application.FLAG_EMAIL,
        "DAYS_EMPLOYED": application.DAYS_EMPLOYED,
        "FLAG_OWN_REALTY": application.FLAG_OWN_REALTY,
        "NAME_HOUSING_TYPE": application.NAME_HOUSING_TYPE,
        "CNT_CHILDREN": application.CNT_CHILDREN,
        "CNT_FAM_MEMBERS": application.CNT_FAM_MEMBERS,
        "NAME_FAMILY_STATUS": application.NAME_FAMILY_STATUS,
        "DAYS_REGISTRATION": application.DAYS_REGISTRATION,
        "DAYS_ID_PUBLISH": application.DAYS_ID_PUBLISH,
        "DAYS_LAST_PHONE_CHANGE": application.DAYS_LAST_PHONE_CHANGE,
        "REG_REGION_NOT_WORK_REGION": application.REG_REGION_NOT_WORK_REGION,
        "REG_CITY_NOT_WORK_CITY": application.REG_CITY_NOT_WORK_CITY,
        "LIVE_CITY_NOT_WORK_CITY": application.LIVE_CITY_NOT_WORK_CITY,
        "NAME_EDUCATION_TYPE": application.NAME_EDUCATION_TYPE,
        "NAME_INCOME_TYPE": application.NAME_INCOME_TYPE,
        "OCCUPATION_TYPE": application.OCCUPATION_TYPE,
        "ORGANIZATION_TYPE": application.ORGANIZATION_TYPE,
        "REGION_RATING_CLIENT": application.REGION_RATING_CLIENT,
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8001/predict",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to communicate with ML service: {str(e)}")

    prediction = db.query(models.Prediction).filter(models.Prediction.application_id == application_id).first()
    if not prediction:
        prediction = models.Prediction(application_id=application_id)
        db.add(prediction)

    prediction.financial_index = result.get("financial_index")
    prediction.behavioral_index = result.get("behavioral_index")
    prediction.digital_trust_index = result.get("digital_trust_index")
    prediction.meta_index = result.get("meta_index")
    prediction.alternative_credit_score = result.get("alternative_credit_score")
    prediction.financial_default_probability = result.get("financial_default_probability")
    prediction.behavioral_default_probability = result.get("behavioral_default_probability")
    prediction.digital_default_probability = result.get("digital_default_probability")
    prediction.overall_default_probability = result.get("overall_default_probability")
    prediction.risk_level = result.get("risk_level")
    prediction.financial_shap_explanations = result.get("financial_shap_explanations")
    prediction.behavioral_shap_explanations = result.get("behavioral_shap_explanations")
    prediction.digital_trust_shap_explanations = result.get("digital_trust_shap_explanations")

    db.commit()
    db.refresh(prediction)

    return result

@router.post("/{application_id}/predict", response_model=ModelResponse)
def predict_endpoint(application_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    app = db.query(models.CreditApplication).filter(models.CreditApplication.id == application_id, models.CreditApplication.user_id == current_user.id).first()
    if not app:
        raise HTTPException(status_code=403, detail="Not authorized or application not found")
    return predict_application(application_id, db)