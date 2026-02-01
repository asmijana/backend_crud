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
│  └─ api/
│     ├─ __init__.py
│     └─ experiments.py   # /experiments endpoints
│     └─ users.py         # /users endpoints
└─ test_experiments.py    # API tests (users + experiments + auth behavior)
   
