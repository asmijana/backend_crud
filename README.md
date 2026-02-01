# Experiment Tracking API

A small but production-style backend service for tracking experiments and their owners.

Built with **FastAPI**, **SQLModel**, and **SQLite**, this project demonstrates:

- RESTful API design with full CRUD
- Database-backed models and relationships
- Simple per-user authorization via a `X-User-Id` header
- Automated tests using `pytest` and FastAPI’s `TestClient`
- A modular, router-based project structure

---

## Features

- **Users**
  - `POST /users` – create a new user
  - `GET /users` – list all users
  - `GET /users/{id}` – fetch a single user
  - `DELETE /users/{id}` – delete a single user

- **Experiments**
  - `POST /experiments/` – create an experiment for the current user
  - `GET /experiments/` – list experiments owned by the current user
  - `GET /experiments/{id}` – fetch a single experiment (only if owned)
  - `PATCH /experiments/{id}` – update an experiment (only if owned)
  - `DELETE /experiments/{id}` – delete an experiment (only if owned)

- **Authorization model (simplified)**
  - Incoming requests pass `X-User-Id` header
  - A dependency (`get_current_user`) loads the corresponding user
  - All experiment operations are scoped to the current user
  - Access to experiments owned by other users returns `403 Forbidden`

This mirrors the structure of real auth (e.g., JWT-based “current user”) without the complexity of a full auth system.

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM / Models:** [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic)
- **Database:** SQLite
- **Testing:** `pytest`, `fastapi.testclient`

---

## Project Structure

```text
.
├─ app/
│  ├─ __init__.py
│  ├─ main.py             # FastAPI app, includes routers
│  ├─ db.py               # engine, init_db, get_session
│  ├─ models.py           # SQLModel DB models (User, Experiment)
│  ├─ schemas.py          # Request/response schemas
│  ├─ deps.py             # Shared dependencies (get_current_user)
│  ├─ test_experiments.py # API tests (users + experiments + auth behavior)
│  └─ api/
│     ├─ __init__.py
│     └─ experiments.py   # /experiments endpoints
│     └─ users.py         # /users endpoints
├─ README.md
├─ LICENSE
├─ experiments.db         # Data stored
└─ requirements.txt       # Requirements listed
```

## How to Run

After cloning, install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
pip install -r requirements.txt
```
For running the API, run the following at the project root:

```bash
uvicorn app.main:app --reload
```
The API will be available at:  

Root: http://127.0.0.1:8000/  
Interactive docs (Swagger UI): http://127.0.0.1:8000/docs  

## Usage Examples

### 1. Creating a user
Endpoint: POST/users

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
        "email": "alpha@example.com",
        "full_name": "Alpha Zenith"
      }'
```
Expected Response:

```bash
{
  "id": 1,
  "email": "alpha@example.com",
  "full_name": "Alpha Zenith"
}
```

### 2. Creating an experiment for that user
Endpoint: POST/experiments

```bash
curl -X POST "http://127.0.0.1:8000/experiments/" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
        "name": "CO2RR test",
        "description": "Screening catalysts for CO2 reduction"
      }'
```
Expected Response:

```bash
{
  "id": 1,
  "name": "CO2RR test",
  "description": "Screening catalysts for CO2 reduction",
  "owner_id": 1
}
```

### 3. List experiments for the current user
Endpoint: GET/experiments

```bash
{
  "id": 1,
  "name": "CO2RR test",
  "description": "Screening catalysts for CO2 reduction",
  "owner_id": 1
}
```
### 4. Attempting to access experiments as another user

First creating another user
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
        "email": "beta@example.com",
        "full_name": "Beta Yan"
      }'
```
Then attempting to access the experiments of another user
```bash
curl -X GET "http://127.0.0.1:8000/experiments/1" \
  -H "X-User-Id: 2"
```
Expected Response:

```bash
{
  "detail": "Not allowed to access this experiment"
}
```
## Running Tests

Tests use an in-memory SQLite database and override the app’s DB session dependency, so they’re fully isolated from your local experiments.db.

From the project root:
```bash
pytest
```

You should see output similar to:
```bash
==================== test session starts ====================
collected X items

tests/test_experiments.py ......
===================== X passed in Y.s =======================
```

## Author

Created by Asmita Jana (asmitajana[at]gmail[dot]com)  
This project was built to experiment with backend features
