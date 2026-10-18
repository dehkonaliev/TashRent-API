# TashRent API

Async REST API for finding apartments and rooms in Tashkent.
Landlords post ads, users search with filters, and a collector adds listings from public Telegram channels.

> Working name. **Status: in development.** See [docs/PLAN.md](docs/PLAN.md) for the roadmap.

**GitHub description (one line):**
Async REST API for finding apartments in Tashkent. FastAPI, PostgreSQL, MongoDB, Redis, OAuth2.

**Topics:** `fastapi` `python` `rest-api` `postgresql` `mongodb` `redis` `sqlalchemy` `pydantic` `oauth2` `asyncio` `docker`

## Why this project

Finding a flat in Tashkent usually means reading hundreds of messy Telegram ads. This project collects them, reads the important details (price, rooms, district, gender preference), removes duplicates, and offers one clean and fast search API.

## Features

- [ ] Register and log in (email + password, Google OAuth2)
- [ ] JWT access tokens and rotating refresh tokens
- [ ] Roles: user, landlord, admin
- [ ] Listings CRUD with filters, sorting and cursor pagination
- [ ] Favorites and saved searches
- [ ] Telegram collector with a text parser for Uzbek and Russian ads
- [ ] Duplicate detection
- [ ] Redis caching and rate limiting
- [ ] Real-time notifications over WebSocket
- [ ] Docker Compose setup, tests and CI

## Tech stack

| Area | Technology |
|---|---|
| Web framework | FastAPI |
| Validation and settings | Pydantic v2, pydantic-settings |
| Relational database | PostgreSQL with SQLAlchemy 2.0 (async) and Alembic |
| Document database | MongoDB (official PyMongo async driver) |
| Cache and messaging | Redis (cache, rate limits, pub/sub) |
| Auth | OAuth2, JWT, Google login |
| Telegram | Telethon |
| Tests | pytest, pytest-asyncio, httpx |
| Tooling | uv, Ruff, pre-commit, Docker, GitHub Actions |

## Architecture

```mermaid
flowchart LR
    TG[Telegram channels] --> C[Collector]
    C --> M[(MongoDB<br/>raw ads)]
    C --> P[(PostgreSQL<br/>listings)]
    C -- new listing event --> R[(Redis)]
    U[Client] --> A[FastAPI REST API]
    A --> P
    A --> R
    R -- pub/sub --> A
    A -- WebSocket --> U
```

The project is a modular monolith with two processes: the **API** and the **collector**. Code is split in layers: routers, services, repositories, schemas and models.

### Why three data stores

| Store | Used for | Reason |
|---|---|---|
| PostgreSQL | Users, listings, favorites, saved searches | Related data that needs constraints and transactions |
| MongoDB | Raw Telegram ads, collector logs | No fixed shape, rarely joined, easy to re-parse later |
| Redis | Search cache, rate limits, revoked tokens, events | Fast and temporary data |

## API overview

Base path: `/api/v1`. Interactive docs: `http://localhost:8000/docs`

| Resource | Endpoints |
|---|---|
| Auth | `POST /auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `GET /auth/google/login` |
| Users | `GET, PATCH, DELETE /users/me` |
| Listings | `GET, POST /listings`, `GET, PATCH, DELETE /listings/{id}` |
| Districts | `GET /districts` |
| Favorites | `GET /users/me/favorites`, `PUT, DELETE /users/me/favorites/{listing_id}` |
| Saved searches | `GET, POST /users/me/saved-searches`, `GET, PATCH, DELETE /users/me/saved-searches/{id}` |
| Notifications | `GET /users/me/notifications`, WebSocket `/ws/notifications` |
| Health | `GET /health`, `GET /health/ready` |

Example request:

```http
GET /api/v1/listings?district=chilonzor&min_price=100&max_price=300&rooms=2&sort=price&limit=20
```

Errors use the Problem Details format (RFC 9457).

## Getting started

**Requirements:** Python 3.12+, [uv](https://docs.astral.sh/uv/), Docker

```bash
git clone <your-repo-url>
cd tashrent-api

cp .env.example .env              # then edit the values
docker compose up -d              # PostgreSQL, MongoDB, Redis

uv sync                           # install dependencies
uv run alembic upgrade head       # create tables
uv run uvicorn app.main:app --reload
```

Run the collector in another terminal:

```bash
uv run python -m collector.main
```

The first run asks for your phone number and a login code from Telegram.

### Environment variables

| Name | Example | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@localhost:5432/tashrent` | PostgreSQL connection |
| `MONGO_URL` | `mongodb://localhost:27017/tashrent` | MongoDB connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `SECRET_KEY` | long random string | Signs JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token life |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `14` | Refresh token life |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | | Google OAuth2 |
| `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` | | From my.telegram.org |
| `CHANNELS` | `@channel_one,@channel_two` | Channels to collect from |
| `USD_UZS` | `12500` | Rate to convert so'm prices |

Never commit `.env` or `*.session` files.

## Running tests

```bash
uv run pytest
uv run ruff check .
```

## Project structure

```
app/            API: routers, services, repositories, models, schemas, parsing
collector/      Telegram collector process
migrations/     Alembic migrations
tests/          unit and integration tests
docs/PLAN.md    roadmap and design notes
```

## Design decisions

- **Layered code:** routers do not touch the database, services do not know HTTP.
- **Raw data is kept:** every Telegram ad is saved in MongoDB, so ads can be re-parsed when the rules improve.
- **Rules, not AI, for parsing:** price, rooms, gender and district are read with text rules. This is free, fast, and easy to test.
- **Rotating refresh tokens:** a stolen refresh token stops working after the real user refreshes.
- **Cursor pagination** for listings, so results stay stable when new ads arrive.

## Privacy and data

Listings from Telegram come from public channels. Each one keeps a link to its source. Phone numbers are not copied.

## Roadmap

Not given for now

## License

Maqsudbek Dehqonaliyev | Python Backend Developer