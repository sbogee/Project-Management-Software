# Project Management Software

A full-stack project management application built with **React**, **FastAPI**, **PostgreSQL**, **Docker**, and **AWS Cloud Services**.

The system allows users to manage projects, collaborate with team members, and upload project documents stored securely in Amazon S3. Uploaded documents are automatically processed through AWS Lambda using an event-driven architecture.

---

# Features

## Authentication

- User registration
- JWT-based authentication
- Protected API endpoints
- Authorization middleware
- Secure user validation

## Project Management

- Create projects
- View owned projects
- View shared projects
- Update project information
- Delete projects
- Project ownership management

## Collaboration

- Invite project members
- Role-based access control
- Participant management
- Owner-specific actions

## Document Management

- Upload documents
- Download documents
- Replace existing documents
- Delete documents
- Project-specific document storage

## AWS Integration

- Amazon S3 document storage
- AWS Lambda document processing
- CloudWatch monitoring
- Event-driven architecture

## Logging

The application logs important business events including:

- User registration
- User login
- Failed login attempts
- Project creation
- Project updates
- Project deletion
- Member invitations
- Document uploads
- Document downloads
- Document deletions

---

# System Architecture

```text
┌─────────────────┐
│ React Frontend  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FastAPI Backend │
└────────┬────────┘
         │
         ├─────────────► PostgreSQL
         │
         ▼
     Amazon S3
         │
         ▼
   AWS Lambda
         │
         ▼
Processed Documents
```

---

# Technology Stack

## Frontend

- React
- React Router
- Bootstrap 5
- JavaScript

## Backend

- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication

## Database

- PostgreSQL 17

## Cloud Services

- Amazon S3
- AWS Lambda
- AWS CloudWatch

## DevOps

- Docker
- Docker Compose

---

# Application Structure

```text
frontend/
│
├── src/
│   ├── pages/
│   ├── components/
│   ├── hooks/
│   └── api/
│
└── public/

app/
|
├── routers/
├── services/
├── schemas/
├── repositories/
├── models/
├── internal/
├── enums/
├── db/
├── core/

tests/

Dockerfile
docker-compose.yml
requirements.txt
```

---

# Backend Architecture

The backend follows a layered architecture.

```text
HTTP Request
      │
      ▼
   Router
      │
      ▼
   Service
      │
      ▼
 Repository
      │
      ▼
 PostgreSQL
```

### Router Layer

Responsible for:

- HTTP request handling
- Authentication dependencies
- Input validation
- Response formatting

### Service Layer

Responsible for:

- Business logic
- Authorization checks
- Workflow orchestration
- Logging

### Repository Layer

Responsible for:

- Database operations
- Query abstraction
- Data persistence

---

# Authentication

The application uses JWT-based authentication.

Authentication flow:

```text
Login
  │
  ▼
JWT Token Generated
  │
  ▼
Stored in Browser
  │
  ▼
Authorization Header
  │
  ▼
Protected Endpoints
```

Example:

```http
Authorization: Bearer <token>
```

---

# Authorization Rules

## Project Owner

Can:

- Create projects
- Modify projects
- Delete projects
- Invite participants
- Upload documents
- Replace documents
- Delete documents

## Participant

Can:

- View project details
- Access project documents
- Upload documents
- Download documents

Cannot:

- Delete projects
- Modify project information
- Invite members

---

# Document Storage

Documents are stored in Amazon S3 instead of the local filesystem.

Each document contains:

```text
filename
s3_key
project_id
uploaded_by
```

Example:

```text
filename:
report.pdf

s3_key:
projects/5/4bc7f618-report.pdf
```

---

# Document Upload Workflow

```text
User Uploads File
        │
        ▼
React Frontend
        │
        ▼
FastAPI Endpoint
        │
        ▼
Amazon S3
        │
        ▼
Store Metadata in PostgreSQL
```

The uploaded file is stored directly in Amazon S3 using boto3.

---

# AWS Lambda Processing

An AWS Lambda function is triggered automatically whenever a new document is uploaded to S3.

Workflow:

```text
Upload File
     │
     ▼
S3 Object Created Event
     │
     ▼
AWS Lambda Triggered
     │
     ▼
Create Processed Copy
     │
     ▼
Store Under:
processed/
```

Example:

```text
projects/1/document.pdf
```

Automatically creates:

```text
processed/projects/1/document.pdf
```

This demonstrates event-driven processing using AWS services.

---

# Logging

The system uses structured logging for important application events.

Examples:

```text
User registered

Successful login

Project created

Member invited

Document uploaded

Project deleted
```

Logging levels:

- INFO
- WARNING
- ERROR

---

# Database Schema

## Users

```text
id
username
hashed_password
```

## Projects

```text
id
name
description
owner_id
```

## Project Members

```text
id
project_id
user_id
```

## Documents

```text
id
filename
s3_key
project_id
uploaded_by
```

---

# Running the Application

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 17
- Docker Desktop

---

# Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```env
DATABASE_URL=
JWT_SECRET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET_NAME=
```

Run:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Docker

Build and start:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

Remove volumes:

```bash
docker compose down -v
```

---

# AWS Configuration

## Amazon S3

Stores uploaded project documents.

Bucket example:

```text
project-management-software-bogi
```

---

## IAM

Application access is configured through:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

---

## AWS Lambda

Triggered by:

```text
S3 ObjectCreated Event
```

Processes newly uploaded files automatically.

---

## CloudWatch

Used for:

- Lambda execution logs
- Event monitoring
- Error tracking

---

# Testing

Run tests:

```bash
pytest
```

The testing layer validates:

- Authentication
- Authorization
- Project management
- Document management
- Service layer logic

---

# Security Features

- Password hashing
- JWT authentication
- Protected endpoints
- Authorization checks
- Project-based permissions
- Secure AWS credential usage via environment variables

---

# Future Improvements

- GitHub Actions CI/CD pipeline
- EC2 deployment
- ECS deployment
- Thumbnail generation for uploaded images
- Document versioning
- Notifications
- Audit history
- User administration panel

---

# Demo Highlights

The most important workflow demonstrated by the application:

```text
User uploads document
          │
          ▼
Amazon S3 stores file
          │
          ▼
S3 Event Trigger
          │
          ▼
AWS Lambda runs automatically
          │
          ▼
Processed document created
```

This demonstrates integration between application code and cloud-native AWS services.

---

# Author

**Boglárka Sándor**

Developed as part of the EPAM Campus Python Specialization program.
