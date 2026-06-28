from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.db import models
from app.core import oauth2
from typing import Dict, Any

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_applications = db.query(func.count(models.CreditApplication.id)).scalar() or 0
    total_predictions = db.query(func.count(models.Prediction.id)).scalar() or 0

    avg_credit_score = db.query(func.avg(models.Prediction.alternative_credit_score)).scalar() or 0
    avg_default_prob = db.query(func.avg(models.Prediction.overall_default_probability)).scalar() or 0

    # Risk level distribution
    risk_distribution = {}
    risk_counts = db.query(
        models.Prediction.risk_level, 
        func.count(models.Prediction.id)
    ).group_by(models.Prediction.risk_level).all()

    for risk_level, count in risk_counts:
        if risk_level:
            risk_distribution[risk_level] = count

    return {
        "total_applications": total_applications,
        "total_predictions": total_predictions,
        "average_credit_score": round(avg_credit_score, 2),
        "average_overall_default_probability": round(avg_default_prob, 4),
        "risk_level_distribution": risk_distribution
    }
