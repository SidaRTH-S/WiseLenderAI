# WiseLenderAI - Backend Gateway Service

This is the central backend API for the WiseLenderAI platform. Built with **FastAPI** and **PostgreSQL**, it serves as the core orchestration layer between the user-facing frontend and the highly specialized Machine Learning inference service (`ml-model`).

## Core Responsibilities

1. **User Authentication & Authorization**: Secure OAuth2 login and JWT-based session management for applicants and lenders.
2. **Loan Application Management**: Provides a robust API for creating, validating, and retrieving comprehensive credit applications containing over 35 unique demographic, financial, and behavioral data points.
3. **Machine Learning Orchestration**: Seamlessly interfaces with the standalone ML-Model service to execute predictive models. It captures the Alternative Credit Score, risk probabilities, and SHAP explainability matrices and persists them in the database.
4. **Analytics & Dashboarding**: Provides aggregated platform insights, including risk distribution and average credit scores, enabling real-time lender dashboards.

---

## Technology Stack

- **Framework**: FastAPI (Python 3)
- **Database ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Database Engine**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens) & OAuth2
- **External Integration**: `requests` for internal microservice communication

---

## Project Structure

```
backend/
│
├── alembic/                # Database migration scripts and versions
├── app/
│   ├── core/               # Core configurations (OAuth2, security)
│   ├── db/                 # Database setup, models, and sessions
│   ├── routers/            # API endpoint definitions
│   │   ├── analytics.py    # Dashboard and aggregate metrics
│   │   ├── auth.py         # Login and token generation
│   │   ├── questionnaire.py# Application management & ML prediction
│   │   └── users.py        # User registration and consent
│   ├── generate.py         # Utility to mock and generate fake applications
│   ├── main.py             # FastAPI application entry point
│   └── schemas.py          # Pydantic models for validation
│
├── .env                    # Environment variables (DB URL, Secrets)
├── alembic.ini             # Alembic configuration
└── requirements.txt        # Python dependencies
```

---

## Installation & Setup

1. **Navigate to the backend directory**:
   ```bash
   cd WiseLenderAI/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Environment**:
   Ensure you have a `.env` file in the root `backend/` directory containing your PostgreSQL database URL and JWT secret keys.
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/wiselender_db
   SECRET_KEY=your_super_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run Database Migrations**:
   The backend uses Alembic to manage database schemas. Run the following command to create all necessary tables:
   ```bash
   alembic upgrade head
   ```

---

## Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Documentation**: `http://127.0.0.1:8000/docs`

> **Note**: For the `/predict` endpoints to work successfully, the separate `ml-model` service must be running concurrently on `http://127.0.0.1:8001`.

---

## Core API Endpoints

### Authentication & Users
- `POST /users/` - Register a new user.
- `PATCH /users/giveconsent/{id}` - Update user data consent.
- `POST /login` - Exchange credentials for a JWT access token.

### Applications & Predictions
- `POST /applications/` - Create and submit a new, detailed loan application.
- `GET /applications/` - Retrieve all applications associated with the currently authenticated user.
- `POST /applications/{id}/predict` - Trigger the ML inference pipeline for a specific application. This will contact the ML service and save the complex prediction indices and SHAP explanations into the database.

### Analytics Dashboard
- `GET /analytics/dashboard` - Returns aggregate statistics for the entire platform (Total applications, average risk, and credit score distributions).

---

## Mock Data Generator

To test the ML pipeline and populate your dashboard without manually filling out 35+ fields, you can use the built-in mock generator.

Run the generator script:
```bash
python -m app.generate
```
*This script will generate a highly realistic, randomized credit application and save it directly to the database.*
