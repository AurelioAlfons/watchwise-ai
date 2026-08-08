# WatchWise AI 🎬

<img width="1846" height="961" alt="image" src="https://github.com/user-attachments/assets/f6ac3602-4809-45cf-8a74-e363e96ba328" />


**AI-powered movie and TV recommendations based on your mood, preferences, and favourite titles.**

[🚀 Live Demo](https://watchwise-ai-puce.vercel.app)

---

## 🛠 Tech Stack

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge\&logo=react\&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge\&logo=typescript\&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge\&logo=tailwind-css\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge\&logo=vercel\&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge\&logo=render\&logoColor=black)

**APIs:** TMDB API · Gemini API / OpenAI

---

## 📖 About

WatchWise AI is a movie and TV recommendation app that helps users decide what to watch based on their mood, preferred genres, and titles they already enjoy.

The project was built to explore how AI can work alongside real external data rather than generating unreliable recommendations. WatchWise only recommends real titles retrieved from TMDB, while AI is used to rank the results and explain why each recommendation fits the user.

---

## ✨ Core Features

* **AI Recommendations** — Get five personalised movie or TV recommendations based on your preferences.
* **Mood & Genre Filtering** — Choose genres, moods, or search for titles similar to something you already enjoyed.
* **Kids Content Filtering** — Restrict recommendations using movie and TV age certifications when watching with children.
* **Real TMDB Data** — Displays real titles, runtime, age ratings, streaming providers, and other TMDB information.
* **AI-Powered Ranking** — Gemini or OpenAI ranks real TMDB candidates instead of inventing movie or TV titles.
* **Automated CI** — GitHub Actions runs backend tests and verifies the frontend build automatically.

---

## ⚙️ How It Works

The **React + TypeScript** frontend sends the user's preferences to a **FastAPI** backend.

The backend searches **TMDB** for real movie or TV candidates based on genre, mood, or a similar title.

An AI model then ranks those candidates and selects the best five recommendations while generating a short explanation for each one.

If kids filtering is enabled, certification data is checked to remove unsuitable or unrated content.

Finally, the backend enriches the selected titles with information such as runtime, age rating, and streaming providers before returning them to the frontend.

The AI never creates fictional titles — it only ranks and explains real TMDB results.

---

## 📌 Project Status

* ✅ AI movie and TV recommendation system
* ✅ TMDB integration and streaming provider data
* ✅ Kids certification filtering
* ✅ Docker support and automated GitHub Actions CI
* ✅ Frontend deployed on Vercel
* ✅ Backend deployed on Render
* 🚧 Improving recommendation filtering and personalisation

---

## 🔮 What's Next

* Add user accounts and saved recommendation history
* Improve personalised recommendations across sessions
* Add more detailed age-based filtering for children
* Improve recommendation variety and filtering
* Add favourites and watchlist functionality

---

## ⚠️ Disclaimer

WatchWise uses TMDB for movie and TV information but is not endorsed or certified by TMDB.

The backend is hosted on a free Render instance and may take around **30–50 seconds** to wake up after a period of inactivity.
