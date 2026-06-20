# WiseLenderAI - ML Model Service

Alternative Credit Scoring Engine.

This service predicts the probability of loan default and generates:

- Default Probability
- Credit Score
- Risk Level
- Top Risk Factors (Explainable AI)

---

# Project Structure

```text
ml-model/
│
├── api/
│   ├── main.py
│   ├── predictor.py
│   └── schemas.py
│
├── models/
│   ├── model_v1.pkl
│   ├── encoders.pkl
│   └── features.pkl
│
├── notebooks/
│   ├── model_training.ipynb
│   ├── model_training1.ipynb
│   └── model_training2.ipynb
│
├── requirements.txt
└── README.md
```

---

# Prerequisites

Install:

- Python 3.12+
- Git

---

# Clone Repository

```bash
git clone #repoURL#
cd WiseLenderAI/ml-model
```

---

# Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Required Files

Ensure these files exist:

```text
models/
├── model_v1.pkl
├── encoders.pkl
└── features.pkl
```

These are generated after model training.

---

# Start API Server

Move to API folder:

```bash
cd api
```

Run:

```bash
uvicorn main:app --reload
```

Server starts on:

```text
http://127.0.0.1:8000
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

This provides an interactive UI for testing the API.

---

# Health Check

Endpoint:

```http
GET /
```

Response:

```json
{
  "status": "running"
}
```

---

# Loan Prediction API

Endpoint:

```http
POST /predict
```

Example Request:

```json
{
  "loan_amnt": 10000,
  "annual_inc": 50000,
  "dti": 15,
  "installment": 300,
  "fico_score": 700,
  "tot_cur_bal": 20000,
  "revol_util": 40,
  "emp_length": 5,
  "home_ownership": "RENT",
  "inq_last_6mths": 1,
  "delinq_2yrs": 0,
  "pct_tl_nvr_dlq": 95,
  "open_acc": 8,
  "total_acc": 20,
  "bc_util": 35,
  "avg_cur_bal": 5000,
  "acc_open_past_24mths": 2,
  "grade": "B",
  "sub_grade": "B3",
  "purpose": "debt_consolidation",
  "verification_status": "Verified",
  "credit_history_years": 10
}
```

---

# Example Response

```json
{
  "default_probability": 0.3891,
  "credit_score": 635,
  "risk_level": "MEDIUM",
  "top_factors": [
    "Credit score history",
    "Detailed credit risk rating",
    "Overall credit grade",
    "Recent account activity",
    "Recent credit inquiries"
  ]
}
```

---

# Risk Levels

| Default Probability | Risk Level |
|--------------------|------------|
| < 0.30 | LOW |
| 0.30 - 0.60 | MEDIUM |
| > 0.60 | HIGH |

---

# Model Information

Algorithm:

```text
XGBoost Classifier
```

Features:

```text
26
```

Outputs:

```text
Default Probability
Credit Score
Risk Category
Explainability Factors
```

Performance:

```text
ROC AUC ≈ 0.73
```

---

# Integration Example

Backend can call:

```http
POST http://localhost:8000/predict
```

and use the JSON response directly.

Workflow:

```text
Frontend
   ↓
Backend
   ↓
ML API
   ↓
Prediction Result
```

---

# Notes

- Dataset is not included in repository.
- Trained model artifacts are required.
- FastAPI automatically validates inputs.
- SHAP is used for explainability.
