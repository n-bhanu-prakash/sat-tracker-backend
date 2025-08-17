# Sat Tracker Backend

A **FastAPI + MongoDB backend** for tracking satellites using the [N2YO API](https://www.n2yo.com/api/).  
This project provides endpoints to fetch:

- Latest TLE (Two-Line Element) data  
- Satellite positions  
- Visual passes  
- Radio passes  
- Satellites currently above a given location  

---

## Project Structure
```
sat-tracker-backend/
│── app/
│ ├── main.py # FastAPI entrypoint
│ ├── core/
│ │ └── config.py # Settings (API key, DB URL, etc.)
│ ├── db/
│ │ └── mongo.py # MongoDB connection + caching
│ ├── models/
│ │ └── schemas.py # Pydantic models (schemas)
│ ├── routers/
│ │ ├── satellites.py # Satellite-related routes
│ │ └── health.py # Health & root endpoints
│ ├── services/
│ │ ├── n2yo_client.py # Handles calls to N2YO API
│ │ └── satellite_service.py # Business logic
│ └── utils/
│ ├── cache.py # Caching helpers
│ └── exceptions.py # Error handling
│
├── .env # Environment variables (N2YO_API_KEY, MONGO_URI, etc.)
├── requirements.txt # Dependencies
└── README.md # Documentation
```

---

## Getting Started

1. Clone the repository
git clone https://github.com/n-bhanu-prakash/sat-tracker-backend.git
cd sat-tracker-backend

2. Create a virtual environment
conda create -n sat-tracker python=3.9 -y
conda activate sat-tracker

3. Install dependencies
pip install -r requirements.txt

4. Configure environment
Create a .env file in the project root:

N2YO_API_KEY=<YOUR_API_KEY>
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=sat_tracker

5. Run the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

API Documentation
Once running, visit:
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc


API Endpoints
Health & Root
| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/`              | Root welcome message |
| GET    | `/api/v1/health` | API health check     |


Satellites
| Method | Endpoint                                     | Query Params                         | Description               |
| ------ | -------------------------------------------- | ------------------------------------ | ------------------------- |
| GET    | `/api/v1/satellites/{norad_id}/tle`          | –                                    | Fetch latest TLE          |
| GET    | `/api/v1/satellites/{norad_id}/positions`    | lat, lng, alt, seconds               | Satellite positions       |
| GET    | `/api/v1/satellites/{norad_id}/visualpasses` | lat, lng, alt, days, min\_visibility | Visual passes             |
| GET    | `/api/v1/satellites/{norad_id}/radiopasses`  | lat, lng, alt, days, min\_elevation  | Radio passes              |
| GET    | `/api/v1/satellites/above`                   | lat, lng, alt, radius, category      | Satellites above location |



Example Usage

Get TLE for the ISS (25544):
curl -X GET "http://127.0.0.1:8000/api/v1/satellites/25544/tle"
