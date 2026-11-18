# Project-Management-Software

## Configuration

Copy `.env.example` to `.env`, set a strong `SECRET_KEY`, and replace the
database password before starting the application. Generate a key with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Keep `.env` private; it is excluded from Git. The same `DATABASE_URL` is used
for local runs, while Docker Compose connects to its `db` service using the
PostgreSQL values in `.env`.
Tokens signed with the previous hardcoded key will no longer be valid.

## Run with Docker Compose

Start the application:

```powershell
docker compose up --build
```

Open the React frontend at [http://localhost:8000](http://localhost:8000). The API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).