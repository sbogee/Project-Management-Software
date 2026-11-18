# Project-Management-Software

## Configuration

Create a root-level `.env` file with `SECRET_KEY`, `DATABASE_URL`,
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, and `S3_BUCKET_NAME`. Set a strong
`SECRET_KEY` and use the same PostgreSQL credentials as your database. Generate
a key with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Keep `.env` private; it is excluded from Git. The same `DATABASE_URL` is used
for local runs, while Docker Compose connects to its `db` service using the
PostgreSQL values in `.env`.
Tokens signed with the previous hardcoded key will no longer be valid.
Docker Compose passes the AWS settings into the API container without copying
`.env` into the image.

## Run with Docker Compose

Start the application:

```powershell
docker compose up --build
```

Open the React frontend at [http://localhost:8000](http://localhost:8000). The API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).