# AI Medicine Recommendation System

FastAPI backend + React (Vite) frontend in a single repo, deployable as one Render web service.

## Structure
```
api/main.py        FastAPI app (also serves the built frontend)
src/               ML pipeline code
models/            trained .pkl models
data/processed/    medicine_information_cleaned.csv
frontend/          React + Vite app
Dockerfile         builds frontend, then runs backend
render.yaml        Render blueprint
```

## Run locally
Backend (project root):
```
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```
Frontend (second terminal):
```
cd frontend
npm install
npm run dev
```
(Vite proxies `/api/*` to `http://127.0.0.1:8000`.)

## Deploy on Render
New + > Web Service > connect this GitHub repo > Runtime: **Docker** > Create.
