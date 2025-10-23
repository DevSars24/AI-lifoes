# AI LifeOS Backend

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-yellowgreen)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-brightgreen)](https://www.mongodb.com/)
[![Redis](https://img.shields.io/badge/Redis-7.0%2B-red)](https://redis.io/)
[![AssemblyAI](https://img.shields.io/badge/AssemblyAI-v0.16%2B-orange)](https://www.assemblyai.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5%2B-purple)](https://ai.google.dev/)

AI LifeOS is a modern, scalable backend API for an AI-powered personal productivity and learning system. It integrates speech-to-text transcription (via AssemblyAI), AI-driven learning suggestions (via Google Gemini), task management, and note-taking with MongoDB persistence and Redis caching. Built with FastAPI for high-performance async APIs, it supports JWT authentication, background tasks, and production deployment via Docker.

## Features

- **Speech Transcription**: Upload audio files and get real-time transcripts with confidence scores.
- **AI Learning Suggestions**: Generate personalized Go programming learning paths with YouTube resources using Gemini.
- **Task Management**: Create, update, and manage tasks with AI interpretation of natural language descriptions.
- **Note-Taking**: CRUD operations for notes with tagging and summarization support.
- **Authentication**: Secure JWT-based auth for protected routes.
- **Caching & Performance**: Redis for fast caching of transcripts and suggestions.
- **Error Handling & Logging**: Structured logging with Loguru and global exception handlers.
- **Production-Ready**: Docker Compose for local/prod setup, NGINX reverse proxy, and health checks.

## Tech Stack

- **Framework**: FastAPI (async APIs, OpenAPI docs)
- **Database**: MongoDB (Motor driver for async ops)
- **Cache**: Redis (async client)
- **AI Services**: AssemblyAI (STT), Google Gemini (generative AI)
- **Auth**: JWT (PyJWT), bcrypt (Passlib)
- **Utils**: Pydantic (schemas/validation), Loguru (logging), aiofiles (async file I/O)
- **Deployment**: Docker, Docker Compose, NGINX

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for prod simulation)
- MongoDB Atlas or local instance
- Redis server
- API keys: AssemblyAI, Google Gemini, Google Cloud (for TTS)

### Installation

1. Clone the repo:
   ```
   git clone https://github.com/DevSars24/ai-lifeos-backend.git
   cd ai-lifeos-backend
   ```

2. Create virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up `.env` (copy from `.env.example`):
   ```
   cp .env.example .env
   ```
   Fill in your values (see Environment Variables below).

5. Run the app:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Access at [http://localhost:8000](http://localhost:8000) and interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### Docker Setup (Production Simulation)

1. Build and run:
   ```
   docker-compose -f app/production/docker-compose.yml up --build
   ```

2. Access via [http://localhost](http://localhost) (NGINX proxy) or directly at [http://localhost:8000](http://localhost:8000).

## Environment Variables

Create `.env` with the following (required for startup):

```
# Database
MONGO_URI=mongodb://localhost:27017/ai_lifeos_db  # Or MongoDB Atlas URI
REDIS_URL=redis://localhost:6379

# AI Services
ASSEMBLYAI_API_KEY=your_assemblyai_key
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
GOOGLE_CLOUD_CREDENTIALS_PATH=/path/to/service_account.json

# JWT Auth
JWT_SECRET=your_super_secret_jwt_key  # Generate: python -c "import secrets; print(secrets.token_hex(32))"
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
FRONTEND_URL=http://localhost:3000  # For CORS
LOG_LEVEL=INFO
```

## API Endpoints

All endpoints are under `/api/`. Use [Swagger UI](http://localhost:8000/docs) for testing.

### Authentication (`/auth`)

- `POST /auth/signup`  
  Body: `{ "email": "user@example.com", "password": "securepass" }`  
  Returns: `{ "access_token": "...", "token_type": "bearer" }`

- `POST /auth/login`  
  Body: `{ "email": "user@example.com", "password": "securepass" }`  
  Returns: JWT token.

Use `Authorization: Bearer <token>` header for protected routes.

### Notes (`/notes`) - Protected

- `GET /notes/` - List all notes
- `POST /notes/` - Create note  
  Body: `{ "title": "My Note", "content": "Content here", "tags": ["tag1"] }`
- `GET /notes/{note_id}` - Get note by ID
- `PATCH /notes/{note_id}` - Update note
- `DELETE /notes/{note_id}` - Delete note

### Tasks (`/tasks`) - Protected (partial)

- `POST /tasks/create` - Create task with AI interpretation  
  Body: `{ "description": "Remind me to code in Go", "priority": "high" }`
- `GET /tasks/` - List tasks
- `GET /tasks/{task_id}` - Get task
- `PATCH /tasks/{task_id}` - Update fields
- `PATCH /tasks/{task_id}/status` - Update status (e.g., "completed")
- `DELETE /tasks/{task_id}` - Delete

### Speech (`/speech`)

- `POST /speech/upload-and-transcribe` - Upload audio file  
  Form: `audio_file` (multipart/form-data)  
  Returns: `{ "transcript_id": "...", "text": "...", "confidence": 0.95, "duration": 10.5 }`

### Learning (`/learning`)

- `POST /learning/suggest`  
  Body: `{ "user_input": "Learn Go concurrency" }`  
  Returns: `{ "suggestion": "Markdown formatted learning path", "resources": ["youtube links"] }`

### Health Check

- `GET /` - Root ping: `{ "message": "AI LifeOS Backend is running ✅" }`
- `GET /health` - Status check (add if needed).

## Project Structure

```
ai-lifeos-backend/
├── app/
│   ├── core/                 # Config, utils, logging, exceptions
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── exception_handler.py
│   │   └── auth_utils.py     # JWT helpers
│   ├── db/                   # Database connections & services
│   │   ├── database.py
│   │   └── db_service.py
│   ├── models/               # Pydantic schemas & Mongo models
│   │   ├── schemas.py
│   │   └── mongo_models.py
│   ├── routers/              # API routes
│   │   ├── notes.py
│   │   ├── tasks.py
│   │   ├── speech.py
│   │   ├── learning.py
│   │   └── auth.py
│   ├── services/             # Business logic
│   │   ├── speech_service.py
│   │   ├── gemini_service.py
│   │   └── auth_service.py
│   ├── utils/                # Helpers (API calls, caching)
│   │   └── api_helper.py
│   └── main.py               # FastAPI app entry
├── app/production/           # Deployment configs
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── nginx.conf
│   ├── start.sh
│   └── .env.production.example
├── logs/                     # Log files
├── .env.example
├── requirements.txt
└── README.md
```

## Future Enhancements

As AI LifeOS evolves, the roadmap focuses on expanding its AI capabilities, improving user experience, enhancing scalability, and integrating more seamless workflows. Below is a detailed, phased plan for future features, prioritized by impact and feasibility. Each enhancement includes a clear explanation of **why** it's valuable, **how** it would be implemented, and **estimated effort** (low/medium/high based on current architecture).

### Phase 1: Core AI Expansions (Next 3-6 Months)
These build directly on existing Gemini and AssemblyAI integrations to make the system smarter and more versatile.

1. **Multi-Language Support for Transcription & Suggestions**  
   - **Why?** Current setup is English-only; global users need support for Hindi, Spanish, etc., to make LifeOS accessible worldwide. This boosts user adoption by 2-3x in non-English markets.  
   - **How?** Update AssemblyAI config to accept `language_code` dynamically (e.g., "hi" for Hindi). For Gemini, add prompt localization. Add a `language` field to schemas like `LearningSuggestionRequest`. Use Redis to cache language-specific prompts.  
   - **Effort:** Medium (API tweaks + testing with diverse audio samples).  
   - **Impact:** High – Enables international users; test with free AssemblyAI tiers.

2. **AI-Powered Note Summarization & Tagging**  
   - **Why?** Users create notes but waste time reviewing; auto-summaries and tags turn raw content into actionable insights, saving 30-50% of review time.  
   - **How?** Extend `gemini_service.py` with a new method `summarize_note(content: str) -> NoteSummaryResponse`. Integrate into `update_note` endpoint as an optional flag. Store summaries in MongoDB `NoteDoc`. Use background tasks for long notes to avoid blocking.  
   - **Effort:** Low (Leverage existing Gemini; add Pydantic response model).  
   - **Impact:** High – Core productivity boost; prototype with sample notes.

3. **Task Prioritization with ML Insights**  
   - **Why?** Current tasks use simple "high/medium/low"; AI can analyze descriptions for urgency (e.g., deadlines) and suggest priorities, reducing decision fatigue.  
   - **How?** In `create_task`, chain Gemini call to extract entities (e.g., dates) and score priority. Add a `suggested_priority` field to `TaskResponse`. Use simple rule-based ML (e.g., regex + Gemini) before full integration with a library like spaCy.  
   - **Effort:** Medium (Prompt engineering + validation).  
   - **Impact:** Medium – Evolves tasks from basic to intelligent.

### Phase 2: User Experience & Integrations (6-12 Months)
Focus on frontend-backend synergy and external tools to create a full ecosystem.

1. **Real-Time Collaboration (WebSockets)**  
   - **Why?** Solo productivity is great, but shared notes/tasks enable team workflows (e.g., study groups for learning suggestions), opening B2B potential.  
   - **How?** Add FastAPI WebSockets endpoint `/ws/notes/{note_id}` for live edits. Use Redis Pub/Sub for broadcasting changes. Protect with JWT via query params. Integrate with frontend via Socket.IO.  
   - **Effort:** High (New protocol + conflict resolution).  
   - **Impact:** High – Transforms from personal to collaborative tool.

2. **TTS (Text-to-Speech) Integration**  
   - **Why?** Read notes/tasks aloud for accessibility (e.g., visually impaired users) or hands-free review, completing the speech loop (STT → Process → TTS).  
   - **How?** Add `tts_service.py` using Google Cloud TTS (leverage existing GCP creds). New endpoint `POST /api/tts/generate` returning audio URLs. Cache audio blobs in S3.  
   - **Effort:** Low (Build on schemas like `TTSRequest`).  
   - **Impact:** Medium – Accessibility win; quick MVP with free GCP quota.

3. **Third-Party Integrations (Calendar, Email)**  
   - **Why?** Tasks/notes should auto-sync to Google Calendar or send email reminders, making LifeOS a central hub instead of isolated.  
   - **How?** Use Celery + Redis for scheduled jobs. Add endpoints like `POST /api/tasks/{task_id}/sync-calendar` with OAuth2 for Google API. Store tokens securely in MongoDB.  
   - **Effort:** High (OAuth flows + error-prone APIs).  
   - **Impact:** High – Increases stickiness; start with Google Workspace.

### Phase 3: Scalability & Advanced Features (12+ Months)
Scale for growth and add cutting-edge AI.

1. **Vector Search for Notes & Suggestions**  
   - **Why?** Semantic search (e.g., "find notes on Go errors") over keyword matching unlocks knowledge discovery in large user data.  
   - **How?** Integrate Pinecone or MongoDB Atlas Vector Search. Embed notes via Gemini embeddings API. Add `/api/search` endpoint with fuzzy queries.  
   - **Effort:** High (New DB index + embedding pipeline).  
   - **Impact:** High – Turns data into a smart knowledge base.

2. **Personalized Analytics Dashboard**  
   - **Why?** Users get insights like "You've completed 80% of high-priority tasks this week" to motivate and refine habits.  
   - **How?** Aggregate MongoDB data with Pandas (via background jobs). Expose via `/api/analytics` endpoint. Use Prometheus for metrics tracking.  
   - **Effort:** Medium (Query optimization + simple viz data).  
   - **Impact:** Medium – Retention booster; visualize with frontend charts.

3. **Mobile Push Notifications**  
   - **Why?** Desktop alerts miss mobile users; real-time reminders (e.g., "Task due now") via FCM keep engagement high.  
   - **How?** Add Firebase integration. Store device tokens in user docs. Trigger via Celery on task status changes.  
   - **Effort:** Medium (New service + permissions).  
   - **Impact:** High – Cross-platform reach.

### Overall Roadmap Rationale
- **Prioritization:** Start with AI depth (Phase 1) for quick wins, then UX (Phase 2) for retention, and scale (Phase 3) for growth.
- **Tech Alignment:** All enhancements reuse existing stack (e.g., Gemini for everything AI) to minimize costs/tech debt.
- **Metrics for Success:** Track via analytics: User retention (+20%), API latency (<200ms), error rates (<1%).
- **Open Source Collaboration:** Community contributions welcome for integrations (e.g., via GitHub Issues).

This roadmap positions AI LifeOS as a full-fledged AI companion, evolving from productivity tool to intelligent ecosystem.

## Deployment

### Local Development

- Use `uvicorn` as above.
- Test with Postman or curl (e.g., `curl -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"pass"}'`).

### Production (Docker + Render/Railway)

1. Update `.env.production` with prod values (e.g., Mongo Atlas URI).
2. Push to GitHub.
3. On Render/Railway: Connect repo, set env vars, build with Dockerfile.
4. For custom domain: Configure NGINX for SSL (Certbot).

Example Render.toml (for Render.com):
```
[build]
  dockerfilePath = "app/production/Dockerfile"

[services]
  httpPort = 8000
  env = "docker"
```

## Testing

- **API Testing**: Use `/docs` for interactive Swagger.
- **Unit Tests**: Add pytest (e.g., `pip install pytest-asyncio pytest-mock`).
  Example test file: `tests/test_notes.py`
  ```
  import pytest
  from fastapi.testclient import TestClient
  from app.main import app

  client = TestClient(app)

  @pytest.mark.asyncio
  async def test_create_note():
      response = client.post("/api/notes/", json={"title": "Test", "content": "Test content"})
      assert response.status_code == 200
  ```
  Run: `pytest tests/`.

- **Load Testing**: Use `locust` or Apache Bench.

## Contributing

1. Fork the repo.
2. Create feature branch: `git checkout -b feature/amazing-feature`.
3. Commit: `git commit -m "feat: add amazing feature"`.
4. Push: `git push origin feature/amazing-feature`.
5. Open PR with description.

Follow PEP 8, add tests, and update docs.

## Built By

This project was built by **Saurabh Singh Rajput**, a passionate backend engineer focused on AI-driven productivity tools. Connect with him for collaborations or feedback:

- [LinkedIn](https://www.linkedin.com/in/saurabh-singh-rajput-25639a306/) – Professional profile and experience.
- [GitHub](https://github.com/DevSars24) – Source code, contributions, and open-source projects.
- [X (Twitter)](https://x.com/SaurabhSin15850) – Updates, tech thoughts, and discussions on AI/backend engineering.

Thanks to Saurabh for architecting this scalable, production-ready backend – from async services to Docker orchestration!

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by FastAPI best practices.
- Thanks to AssemblyAI & Google for AI integrations.
- Built with ❤️ by Saurabh Singh Rajput 

---

*Questions? Open an issue or ping @SaurabhSin15850 on X.*
