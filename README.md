**Sat Tracker Backend**

A FastAPI + MongoDB backend for tracking satellites using the N2YO API.
This project supports fetching TLE data, satellite positions, passes (visual/radio), and satellites currently above a location.

**PROJECT_STRUCTURE**

sat-tracker-backend/
│── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── core/
│   │   └── config.py         # Settings (API key, DB URL, etc.)
│   ├── db/
│   │   └── mongo.py          # MongoDB connection + caching
│   ├── models/
│   │   └── satellite.py      # Pydantic models (schemas)
│   ├── services/
│   │   └── n2yo_service.py   # Handles calls to N2YO API
│   ├── api/
│   │   ├── routes_satellites.py # Satellite-related routes
│   │   └── routes_default.py    # Health & root endpoints
│   └── __init__.py
│
├── .env                      # Environment variables (N2YO_API_KEY, MONGO_URI, etc.)
├── requirements.txt          # Dependencies
└── README.md                 # Docs



**Clone the repository**
git clone https://github.com/<your-username>/sat-tracker-backend.git
cd sat-tracker-backend


**Create virtual environment**
conda create -n sat-tracker python=3.9 -y
conda activate sat-tracker




**Install dependencies**
pip install -r requirements.txt


**Configure environment**
N2YO_API_KEY=<YOUR_API_KEY>
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=sat_tracker


**Run FastAPI server**
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


Visit:

Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc



**API Endpoints**
<Health & Root>
| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/`              | Root welcome message |
| GET    | `/api/v1/health` | API health check     |

<Satellite Data>


| Method | Endpoint                                     | Query Params                      | Description               |
| ------ | -------------------------------------------- | --------------------------------- | ------------------------- |
| GET    | `/api/v1/satellites/{norad_id}/tle`          | –                                 | Fetch latest TLE          |
| GET    | `/api/v1/satellites/{norad_id}/positions`    | `lat,lng,alt,seconds`             | Satellite positions       |
| GET    | `/api/v1/satellites/{norad_id}/visualpasses` | `lat,lng,alt,days,min_visibility` | Visual passes             |
| GET    | `/api/v1/satellites/{norad_id}/radiopasses`  | `lat,lng,alt,days,min_elevation`  | Radio passes              |
| GET    | `/api/v1/satellites/above`                   | `lat,lng,alt,radius,category`     | Satellites above location |



<Example Usage>
Get TLE for ISS
curl -X GET "http://127.0.0.1:8000/api/v1/satellites/25544/tle"
