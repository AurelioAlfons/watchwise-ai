# WatchWise AI 🎬
WatchWise AI recommends movies or TV shows based on your mood and preferences.

## Live Demo
- Frontend: https://watchwise-ai-puce.vercel.app
- Backend: https://watchwise-ai.onrender.com

Note: the backend is on a free instance and may take ~30-50s to wake up if inactive.

## Features
- Movie and TV recommendations
- AI-generated reasons
- TMDB movie data
- Streaming providers
- Docker support
- Automated GitHub Actions
- Deployed on Render (backend) + Vercel (frontend)

## Tech Stack
- React + TypeScript
- Tailwind CSS
- FastAPI
- Python 3.11
- TMDB API
- Gemini API
- Docker

---

## Project Structure
```text
watchwise-ai/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

### Backend (`backend/.env`)
```env
TMDB_API_KEY=your_tmdb_api_key
GEMINI_API_KEY=your_gemini_api_key
AI_PROVIDER=gemini
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:8000
```

---

## Run Locally

### Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend:
```
http://localhost:5173
```
Backend:
```
http://localhost:8000
```

---

## Run with Docker
```bash
docker compose up --build
```
Frontend:
```
http://localhost:3000
```
Backend:
```
http://localhost:8000
```

---

## Run Tests
```bash
cd backend
$env:PYTHONPATH="."
pytest
```

---

## Deployment
- Backend deployed on **Render** (Docker Web Service), root directory `backend`
- Frontend deployed on **Vercel**, root directory `frontend`
- Env vars (`TMDB_API_KEY`, `GEMINI_API_KEY`, `CORS_ORIGINS`) are set directly in Render's dashboard, not committed
- `VITE_API_URL` is set in Vercel's dashboard and points to the live Render backend

---

## Notes
- No login or database (MVP)
- Uses TMDB for movie data
- Uses Gemini to rank and explain recommendations
- API keys are stored in `.env` / hosting dashboards and are **not** committed to GitHub
