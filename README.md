# MindTrack

> B2B SaaS platform for freelance psychologists and counselors in India.

## Project Structure

```
mindtrack/
├── backend/               # FastAPI REST API
│   ├── main.py            # Application entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── core/          # Config, DB, security, dependencies
│       ├── models/        # SQLAlchemy ORM models
│       ├── schemas/       # Pydantic request/response schemas
│       ├── routers/       # FastAPI route handlers
│       ├── services/      # Business logic layer
│       ├── tasks/         # Celery background tasks
│       └── utils/         # R2 storage, pagination helpers
├── frontend/              # Next.js 14 App Router
│   ├── app/
│   │   ├── (auth)/        # Login & Register pages
│   │   └── (dashboard)/   # Protected dashboard
│   ├── lib/               # API client, auth helpers
│   └── middleware.ts      # Route protection
├── docker-compose.yml
├── .env.example
└── README.md
```

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI, Python 3.11+, async      |
| Database  | Supabase (PostgreSQL + pgvector)  |
| Cache     | Upstash Redis                     |
| Storage   | Cloudflare R2                     |
| Auth      | JWT (python-jose) + bcrypt        |
| Queue     | Celery + Upstash Redis broker     |
| Frontend  | Next.js 14, TypeScript, Tailwind  |

## Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy and fill in environment variables
cp .env.example .env

# Run the server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local

# Add to .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

### Docker Compose

```bash
# From project root
cp .env.example .env
# Fill in all values in .env

docker-compose up --build
```

## Supabase Setup

1. Create a project at [supabase.com](https://supabase.com)
2. Go to **Settings > Database** and copy the connection string
3. Replace `[YOUR-PASSWORD]` in the connection string
4. Set `SUPABASE_DB_URL` using the `postgresql+asyncpg://` scheme
5. Database tables are managed via Supabase MCP — no migrations needed

## API Endpoints

| Method | Endpoint                         | Description            |
|--------|----------------------------------|------------------------|
| POST   | `/api/v1/auth/register`          | Register counselor     |
| POST   | `/api/v1/auth/login`             | Login                  |
| POST   | `/api/v1/auth/refresh`           | Refresh JWT            |
| GET    | `/api/v1/auth/me`                | Get profile            |
| CRUD   | `/api/v1/patients`               | Patient management     |
| CRUD   | `/api/v1/appointments`           | Appointment management |
| CRUD   | `/api/v1/locations`              | Location management    |
| CRUD   | `/api/v1/notes`                  | Session notes          |
| CRUD   | `/api/v1/finance/transactions`   | Financial records      |
| GET    | `/api/v1/subscriptions/me`       | View subscription      |

## Deploy

### Backend → Railway

1. Connect GitHub repo to [Railway](https://railway.app)
2. Set root directory to `backend`
3. Add all environment variables from `.env.example`
4. Railway auto-detects `Dockerfile` and deploys
5. Set up a custom domain or use the Railway URL

### Frontend → Vercel

1. Connect GitHub repo to [Vercel](https://vercel.com)
2. Set root directory to `frontend`
3. Set `NEXT_PUBLIC_API_URL` to your Railway backend URL
4. Deploy — Vercel auto-detects Next.js

## License

Private — All rights reserved.
