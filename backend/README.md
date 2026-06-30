# Sdrama123 Backend

FastAPI backend for the Sdrama123 public movie website and admin dashboard.

This backend is designed to support:

- User authentication and roles
- Admin dashboard summaries
- Movie creation, uploads, and publishing
- Series, season, and episode management
- Poster, video, and subtitle file uploads
- Genres and categories
- Views, favorites, and analytics
- App settings
- PostgreSQL database storage

## Architecture

```text
Users
  |
  |-- Frontend Website
  |-- Admin Dashboard
          |
          v
   FastAPI Backend
          |
  ---------------------
  | Auth              |
  | Content Service   |
  | Analytics         |
  | Settings          |
  ---------------------
          |
          v
      PostgreSQL
          |
  ---------------------
  | Video Storage     |
  | Subtitle Files    |
  | Poster Images     |
  ---------------------
```

## What Has Been Implemented

The backend folder has been created with a modular FastAPI structure:

```text
backend/
  app/
    api/
    auth/
    categories/
    core/
    dashboard/
    db/
    genres/
    movies/
    series/
    settings/
    shared/
    subtitles/
    users/
    analytics/
    main.py
  storage/uploads/
  .env.example
  requirements.txt
  README.md
```

Implemented backend pieces:

- FastAPI app entrypoint in `app/main.py`
- PostgreSQL SQLAlchemy database setup in `app/db/session.py`
- Environment config in `app/core/config.py`
- Shared SQLAlchemy models in `app/shared/models.py`
- Shared Pydantic schemas in `app/shared/schemas.py`
- File upload helper in `app/shared/files.py`
- API router aggregation in `app/api/router.py`
- Authentication routes
- User/admin routes
- Movie CRUD and upload routes
- Series, season, and episode routes
- Genre and category routes
- Subtitle listing route
- Analytics routes for views and favorites
- Dashboard summary route
- Settings routes
- Static `/uploads` mount for uploaded files

## Database Tables

The SQLAlchemy models currently define these tables:

- `users`
- `roles`
- `user_roles`
- `movies`
- `series`
- `seasons`
- `episodes`
- `genres`
- `categories`
- `subtitles`
- `views`
- `favorites`
- `settings`

Tables are created automatically on app startup with `Base.metadata.create_all(...)`. Later, this should be replaced with Alembic migrations before production.

## Setup

Create a Python virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create an environment file:

```bash
cp .env.example .env
```

Create a PostgreSQL database:

```bash
createdb sdrama123
```

Then update `DATABASE_URL` in `.env` if your PostgreSQL username, password, host, or database name is different.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/sdrama123
```

## Run The Backend

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Important API Routes

Authentication:

- `POST /api/auth/register`
- `POST /api/auth/login`

Dashboard:

- `GET /api/dashboard/summary`

Users:

- `GET /api/users`
- `PATCH /api/users/{user_id}/status`

Movies:

- `GET /api/movies`
- `POST /api/movies`
- `GET /api/movies/{movie_id}`
- `PATCH /api/movies/{movie_id}`
- `PATCH /api/movies/{movie_id}/publish`
- `POST /api/movies/{movie_id}/poster`
- `POST /api/movies/{movie_id}/video`
- `POST /api/movies/{movie_id}/subtitles`

Series:

- `GET /api/series`
- `POST /api/series`
- `PATCH /api/series/{series_id}`
- `PATCH /api/series/{series_id}/publish`
- `POST /api/series/{series_id}/poster`
- `POST /api/series/{series_id}/seasons`
- `GET /api/series/{series_id}/seasons`
- `POST /api/series/seasons/{season_id}/episodes`
- `PATCH /api/series/episodes/{episode_id}`
- `PATCH /api/series/episodes/{episode_id}/publish`
- `POST /api/series/episodes/{episode_id}/poster`
- `POST /api/series/episodes/{episode_id}/video`
- `POST /api/series/episodes/{episode_id}/subtitles`

Genres and categories:

- `GET /api/genres`
- `POST /api/genres`
- `GET /api/categories`
- `POST /api/categories`

Subtitles:

- `GET /api/subtitles`

Analytics:

- `POST /api/analytics/views`
- `POST /api/analytics/favorites`
- `DELETE /api/analytics/favorites/{favorite_id}`
- `GET /api/analytics/summary`

Settings:

- `GET /api/settings`
- `PUT /api/settings/{key}`

## Upload Flow

Movie admin flow:

```text
Create Movie
  -> Upload Poster
  -> Upload Video
  -> Upload Subtitles
  -> Publish
```

Series admin flow:

```text
Create Series
  -> Upload Series Poster
  -> Create Season
  -> Create Episode
  -> Upload Episode Poster
  -> Upload Episode Video
  -> Upload Subtitle
  -> Publish Episode
```

Uploaded files are saved under:

```text
backend/storage/uploads/
```

The backend exposes uploaded files through:

```text
/uploads
```

## Auth Notes

Authentication uses:

- Password hashing with `passlib`
- JWT tokens with `python-jose`
- Bearer token auth
- Admin-only route protection through the `admin` role

Admin-protected routes require a logged-in user with an `admin` role.

## Current Status

Done:

- Backend project structure created
- FastAPI app created
- SQLAlchemy PostgreSQL models created
- Pydantic schemas created
- Auth/register/login implemented
- Admin-protected routes added
- Movie and series upload routes added
- Analytics and dashboard routes added
- README and `.env.example` added

Not done yet:

- Frontend admin forms are not connected to this API yet
- Public website watch/favorite actions are not connected yet
- PostgreSQL database has not been created or tested locally
- Alembic migrations are not added yet
- Real file validation, file size limits, and cloud storage are not added yet
- Production security settings are not finalized

## Next Steps

Recommended next backend tasks:

1. Create the PostgreSQL database.
2. Run the backend and open `/docs`.
3. Create the first admin user with `POST /api/auth/register`.
4. Connect the admin dashboard forms to the movie and series endpoints.
5. Add Alembic migrations.
6. Add stricter upload validation for poster, video, and subtitle files.
