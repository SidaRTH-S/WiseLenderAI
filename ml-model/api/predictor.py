import joblib
import pandas as pd
import shap

model = joblib.load("../models/model_v1.pkl")
encoders = joblib.load("../models/encoders.pkl")
features = joblib.load("../models/features.pkl")
explainer = shap.TreeExplainer(model)


def risk_to_credit_score(prob):
    return int(
        300 + (1 - prob) * 550
    )


def risk_level(prob):
    if prob < 0.20:
        return "LOW"
    elif prob < 0.50:
        return "MEDIUM"
    return "HIGH"


def explain_feature(feature):
    mapping = {
        "fico_score": "Credit score history",
        "sub_grade": "Detailed credit risk rating",
        "grade": "Overall credit grade",
        "inq_last_6mths": "Recent credit inquiries",
        "delinq_2yrs": "Past delinquencies",
        "loan_amnt": "Requested loan amount",
        "annual_inc": "Annual income",
        "dti": "Debt-to-income ratio",
        "acc_open_past_24mths": "Recent account activity",
        "emp_length": "Employment stability",
        "credit_history_years": "Length of credit history"
    }
    return mapping.get(feature, feature)


def predict(data):
    df = pd.DataFrame([data])
    df["loan_income_ratio"] = (
        df["loan_amnt"] /
        (df["annual_inc"] + 1)
    )
    df["balance_income_ratio"] = (
        df["tot_cur_bal"] /
        (df["annual_inc"] + 1)
    )
    df["accounts_per_year"] = (
        df["total_acc"] /
        (df["credit_history_years"] + 1)
    )
    df["credit_utilization_score"] = (
        df["revol_util"] *
        df["bc_util"]
    )
    for col in encoders:
        df[col] = encoders[col].transform(
            df[col]
        )
    df = df[features]
    prob = model.predict_proba(df)[0][1]
    shap_values = explainer.shap_values(df)
    shap_df = pd.DataFrame({
        "feature": df.columns,
        "impact": shap_values[0]
    })
    shap_df["abs_impact"] = (
        shap_df["impact"].abs()
    )
    shap_df = shap_df.sort_values(
        "abs_impact",
        ascending=False
    )
    top_factors = [
    explain_feature(f)
    for f in shap_df.head(5)["feature"]
    ]
    return {
            "default_probability": float(prob),
            "credit_score": risk_to_credit_score(prob),
            "risk_level": risk_level(prob),
            "top_factors": top_factors
    }