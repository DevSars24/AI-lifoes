# AI-LifeOS Backend

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-brightgreen)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)](https://www.mongodb.com/atlas)

AI-LifeOS is an intelligent backend platform designed to supercharge your daily life with AI-powered tools. Built with FastAPI for blazing-fast APIs, it integrates Google's Gemini for smart content generation, speech-to-text/tts for voice interactions, and MongoDB for seamless data management. Whether you're managing tasks, taking notes, learning new skills, or transcribing audio, AI-LifeOS handles it all with privacy and efficiency in mind.

## 🚀 Features

- **Task Management**: Create, update, and track AI-assisted tasks with natural language processing.
- **Smart Notes**: Generate, organize, and summarize notes using Gemini AI.
- **Learning Hub**: Personalized learning paths with AI-generated quizzes and explanations.
- **Speech Services**: Real-time speech-to-text transcription and text-to-speech synthesis.
- **Secure Auth**: JWT-based authentication with role-based access.
- **Scalable Architecture**: Docker-ready for easy deployment, with Nginx for production serving.
- **Testing Suite**: Pytest coverage for services, routers, and database interactions.


```
## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI |
| **Database** | MongoDB (via PyMongo/Motor) |
| **AI/ML** | Google Gemini API |
| **Speech** | Google Cloud Speech-to-Text & Text-to-Speech |
| **Auth** | JWT (PyJWT) |
| **Deployment** | Docker, Docker Compose, Nginx |
| **Testing** | Pytest |
| **Logging** | Python logging with file rotation |

## 📦 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB Atlas account (free tier works)
- Google Cloud credentials for Gemini and Speech APIs

### 1. Clone & Install
```bash
git clone https://github.com/DevSars24/ailifeos.git
cd ailifeos/ai-lifeos-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup
Copy the example env:
```bash
cp app/production/.env.production.example .env
```
Edit `.env` with your secrets (e.g., `MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/db`, `GEMINI_API_KEY=your_key`).

### 3. Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

### 4. Test an Endpoint
```bash
curl -X GET "http://localhost:8000/tasks/health" -H "accept: application/json"
```
Response: `{"status": "AI-LifeOS backend is alive! 🚀"}`

## 🏗 Project Structure

```
ai-lifeos-backend/
├── app/
│   ├── core/          # Config, utils, logger, exception handlers
│   ├── db/            # Database connections (MongoDB)
│   ├── models/        # Pydantic schemas & Mongo models
│   ├── routers/       # API endpoints (auth, learning, notes, speech, tasks)
│   ├── services/      # Business logic (DB, Gemini, speech, TTS, auth)
│   └── main.py        # FastAPI app entrypoint
├── tests/             # Unit/integration tests
├── app/production/    # Dockerfiles, Nginx config, prod scripts (ignored secrets)
├── logs/              # Application logs
├── requirements.txt   # Dependencies
└── .gitignore         # Ignores env files, caches, logs
```

## 🔐 Security & Best Practices
- **Secrets**: Never commit `.env` files—use placeholders in examples.
- **Rate Limiting**: Integrated via FastAPI middleware (extend as needed).
- **CORS**: Configured for frontend integration.
- **Validation**: Pydantic for robust input/output schemas.

## 🧪 Testing
Run tests:
```
pytest tests/ -v
```
Coverage: `pytest --cov=app/services --cov-report=html`

## 🌐 Deployment

### Docker Local
```bash
cd app/production
docker-compose up -d
```

### Production (e.g., AWS/EC2)
1. Build: `docker build -t ai-lifeos-backend .`
2. Run with env vars: `docker run -p 80:80 -e MONGODB_URI=... ai-lifeos-backend`
3. Use Nginx for reverse proxy (see `app/production/nginx.conf`).

## 🤝 Contributing
1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Commit: `git commit -m "Add amazing feature"`.
4. Push: `git push origin feature/amazing-feature`.
5. Open a Pull Request!

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
This project is MIT licensed. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework.
- [Google Gemini](https://ai.google.dev/) for AI magic.
- [MongoDB Atlas](https://www.mongodb.com/atlas) for cloud DB.

---



3. Commit: `git add README.md && git commit -m "Add comprehensive README" && git push`.

If you want badges updated, more sections (e.g., API examples), or tweaks, just say! 🚀
