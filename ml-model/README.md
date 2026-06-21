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

---

# Input Field Reference

| Field | Type | Allowed Values / Range | Description | Example |
|--------------------------|---------|------------------------------------|-------------------------------------------------------------|----------------|
| loan_amnt | float | > 0 | Total loan amount requested by the applicant (in local currency). | 10000 |
| annual_inc | float | > 0 | Applicant's annual income before taxes. | 50000 |
| dti | float | 0 - 100 | Debt-to-Income Ratio (%). Lower values indicate better repayment capacity. | 15 |
| installment | float | > 0 | Expected monthly loan installment payment. | 300 |
| fico_score | float | 300 - 850 | Credit score representing applicant's creditworthiness. Higher is better. | 700 |
| tot_cur_bal | float | >= 0 | Total outstanding balance across all current credit accounts. | 20000 |
| revol_util | float | 0 - 100 | Revolving credit utilization percentage. Lower utilization is generally better. | 40 |
| emp_length | integer | 0 - 50 | Number of years the applicant has been employed. | 5 |
| home_ownership | string | RENT, OWN, MORTGAGE, OTHER | Current housing status of the applicant. | RENT |
| inq_last_6mths | integer | >= 0 | Number of credit inquiries made in the last six months. | 1 |
| delinq_2yrs | integer | >= 0 | Number of delinquent credit payments in the last two years. | 0 |
| pct_tl_nvr_dlq | float | 0 - 100 | Percentage of credit accounts that have never been delinquent. Higher is better. | 95 |
| open_acc | integer | >= 0 | Total number of currently open credit accounts. | 8 |
| total_acc | integer | >= open_acc | Total number of credit accounts ever opened by the applicant. | 20 |
| bc_util | float | 0 - 100 | Bankcard utilization percentage. Lower values indicate better credit management. | 35 |
| avg_cur_bal | float | >= 0 | Average balance maintained across all active credit accounts. | 5000 |
| acc_open_past_24mths | integer | >= 0 | Number of new credit accounts opened in the last 24 months. | 2 |
| grade | string | A, B, C, D, E, F, G | Overall lending risk grade assigned to the applicant. A is lowest risk and G is highest risk. | B |
| sub_grade | string | A1-A5, B1-B5, C1-C5, D1-D5, E1-E5, F1-F5, G1-G5 | Detailed risk category within each grade. A1 represents the best credit quality while G5 represents the highest risk. | B3 |
| purpose | string | car, credit_card, debt_consolidation, educational, home_improvement, house, major_purchase, medical, moving, other, renewable_energy, small_business, vacation, wedding | Primary purpose for which the loan is requested. | debt_consolidation |
| verification_status | string | Verified, Source Verified, Not Verified | Indicates whether the applicant's income has been verified by the lender or a third party. | Verified |
| credit_history_years | float | >= 0 | Total length of the applicant's credit history in years. Longer history generally indicates more reliable credit behavior. | 10 |

---
# Frontend Recommendations

| Field | UI Component |
|------------------------|----------------|
| loan_amnt | Number Input |
| annual_inc | Number Input |
| dti | Slider / Number Input |
| installment | Number Input |
| fico_score | Number Input |
| tot_cur_bal | Number Input |
| revol_util | Slider (0-100) |
| emp_length | Number Input |
| home_ownership | Dropdown |
| inq_last_6mths | Number Input |
| delinq_2yrs | Number Input |
| pct_tl_nvr_dlq | Slider (0-100) |
| open_acc | Number Input |
| total_acc | Number Input |
| bc_util | Slider (0-100) |
| avg_cur_bal | Number Input |
| acc_open_past_24mths | Number Input |
| grade | Dropdown |
| sub_grade | Dropdown |
| purpose | Dropdown |
| verification_status | Dropdown |
| credit_history_years | Number Input |

---


# Allowed Values

## home_ownership

```text
RENT
OWN
MORTGAGE
OTHER
```

| Value | Meaning |
|------------|-----------------------------|
| RENT | Applicant lives in a rented house |
| OWN | Applicant owns the house |
| MORTGAGE | House is under mortgage |
| OTHER | Any other housing arrangement |

---

## grade

```text
A
B
C
D
E
F
G
```

| Grade | Risk Level |
|------------|----------------|
| A | Lowest Risk |
| B | Low Risk |
| C | Moderate Risk |
| D | Medium Risk |
| E | High Risk |
| F | Very High Risk |
| G | Highest Risk |

---

## sub_grade

```text
A1 A2 A3 A4 A5
B1 B2 B3 B4 B5
C1 C2 C3 C4 C5
D1 D2 D3 D4 D5
E1 E2 E3 E4 E5
F1 F2 F3 F4 F5
G1 G2 G3 G4 G5
```

Each grade is divided into five finer risk levels.

Example:

```text
A1 -> Best credit quality
A5 -> Weakest within Grade A
B1 -> Better than B5
G5 -> Highest estimated risk
```

---

## purpose

```text
car
credit_card
debt_consolidation
educational
home_improvement
house
major_purchase
medical
moving
other
renewable_energy
small_business
vacation
wedding
```

| Value | Description |
|------------------------|---------------------------|
| car | Vehicle purchase |
| credit_card | Credit card repayment |
| debt_consolidation | Combine multiple debts |
| educational | Education expenses |
| home_improvement | Home renovation |
| house | House purchase |
| major_purchase | Large purchase |
| medical | Medical expenses |
| moving | Relocation expenses |
| other | Miscellaneous purpose |
| renewable_energy | Solar/green energy |
| small_business | Business funding |
| vacation | Travel expenses |
| wedding | Marriage expenses |

---

## verification_status

```text
Verified
Source Verified
Not Verified
```

| Value | Meaning |
|-----------------|--------------------------------|
| Verified | Income verified by lender |
| Source Verified | Verified through third-party source |
| Not Verified | Income not verified |

---

# API Response Schema

## Success Response

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

### Response Fields

| Field | Type | Description |
|------------------------|-------------|------------------------------------------------------|
| default_probability | float | Predicted probability of loan default (0.0 - 1.0) |
| credit_score | integer | Generated credit score between 300 and 850 |
| risk_level | string | Overall risk category (`LOW`, `MEDIUM`, `HIGH`) |
| top_factors | array[string] | Top factors influencing the prediction |

---

## Risk Level Interpretation

| Default Probability | Risk Level | Description |
|----------------------|------------|--------------------------------|
| 0.00 - 0.30 | LOW | Low probability of default |
| 0.30 - 0.60 | MEDIUM | Moderate probability of default |
| 0.60 - 1.00 | HIGH | High probability of default |

---

## Credit Score Interpretation

| Credit Score | Rating |
|--------------|----------------|
| 800 - 850 | Exceptional |
| 740 - 799 | Very Good |
| 670 - 739 | Good |
| 580 - 669 | Fair |
| 300 - 579 | Poor |

---

## Error Response

```json
{
  "detail": [
    {
      "loc": ["body", "loan_amnt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

or

```json
{
  "detail": "Invalid categorical value: home_ownership must be one of [RENT, OWN, MORTGAGE, OTHER]"
}
```

---

## Backend Integration Notes

- All numeric fields must be sent as JSON numbers (`int` or `float`).
- All categorical fields are **case-sensitive** and must exactly match the allowed values listed above.
- The API returns responses in JSON format.
- `default_probability` ranges from **0.0 to 1.0**.
- `credit_score` is automatically derived from the predicted default probability.
- `top_factors` provides an explainable AI summary highlighting the most influential features affecting the prediction.

