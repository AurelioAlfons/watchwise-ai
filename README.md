# WatchWise AI 🎬
WatchWise AI recommends movies or TV shows based on your mood and preferences.

## Live Demo
- Frontend: https://watchwise-ai-puce.vercel.app
- Backend: https://watchwise-ai.onrender.com

Note: the backend is on a free instance and may take ~30-50s to wake up if inactive.

## Features
- Movie and TV recommendations
- AI-generated reasons, powered by real TMDB candidate data (never invented titles)
- Genre and mood selection, plus "similar to a title you loved" search
- Content filtering by age certification when watching with kids
- TMDB movie data, streaming providers, runtime, and age ratings
- Docker support
- Automated GitHub Actions CI (backend tests + frontend build)
- Deployed on Render (backend) + Vercel (frontend)

## Tech Stack
- React + TypeScript + Tailwind CSS
- FastAPI + Python 3.11
- TMDB API
- Gemini API (or OpenAI, configurable)
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

## How Recommendations Work
1. **Search** — TMDB finds real candidate titles based on genre, or via TMDB's own similarity/recommendation graph if a "similar to" title is given
2. **Rank** — an AI model picks the best 5 from that real candidate pool and explains why, prioritizing variety over same-franchise picks
3. **Filter** — if "watching with kids" is selected, results are restricted to G/PG (movies) or TV-Y/TV-Y7/TV-G/TV-PG (TV), based on TMDB certification data. Titles with no rating data are excluded rather than risked.
4. **Enrich** — runtime, age rating, and streaming providers are attached to the final 5 picks

The AI never invents titles — it only ranks and explains real TMDB data.

---

## Environment Variables

### Backend (`backend/.env`)
```env
TMDB_API_KEY=your_tmdb_api_key
GEMINI_API_KEY=your_gemini_api_key
AI_PROVIDER=gemini
WATCH_REGION=AU
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
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
pytest -v
```
Covers AI response parsing (malformed/wrapped JSON handling) and kids content certification filtering.

---

## Deployment
- Backend deployed on **Render** (Docker Web Service), root directory `backend`
- Frontend deployed on **Vercel**, root directory `frontend`
- Env vars (`TMDB_API_KEY`, `GEMINI_API_KEY`, `CORS_ORIGINS`, `WATCH_REGION`) are set directly in Render's dashboard, not committed
- `VITE_API_URL` is set in Vercel's dashboard and points to the live Render backend

---

## Known Limitations
- "Watching with kids" applies one broad certification cutoff (PG/TV-PG and under), not age-tiered filtering
- Certification filtering for TV shows and "similar to" searches happens after the AI ranking step (TMDB doesn't support certification filtering on those endpoints), so a kids-filtered request may occasionally return fewer than 5 results
- No login or database (MVP) — no saved history or personalization across sessions

---

## Notes
- Uses TMDB for movie/show data and streaming availability
- Uses Gemini (or OpenAI) to rank and explain recommendations from real TMDB candidates
- API keys are stored in `.env` / hosting dashboards and are **not** committed to GitHub
