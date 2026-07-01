# WatchWise AI 🎬

WatchWise AI recommends movies or TV shows based on your mood and preferences.

## Features

- Movie and TV recommendations
- AI-generated reasons
- TMDB movie data
- Streaming providers
- Docker support
- Automated GitHub Actions

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

## Notes

- No login or database (MVP)
- Uses TMDB for movie data
- Uses Gemini to rank and explain recommendations
- API keys are stored in `.env` and are **not** committed to GitHub
