# Software Design Document (SDD)

## Project Management Software

**Author:** Boglárka Sándor  
**Technology Stack:** React, FastAPI, PostgreSQL, Docker, AWS S3, AWS Lambda  
**Version:** 1.0

---

# 1. Introduction

## 1.1 Purpose

The purpose of this document is to describe the architecture, design decisions, components, and workflows of the Project Management Software application.

The system enables users to:

- Create and manage projects
- Collaborate with project members
- Manage project documents
- Store documents securely in Amazon S3
- Automatically process uploaded files using AWS Lambda

---

## 1.2 Scope

The application provides:

- User authentication
- Project management
- Participant management
- Document management
- Cloud-based storage
- Event-driven document processing

---

# 2. System Overview

The Project Management Software is a full-stack web application designed around a layered backend architecture and a component-based frontend architecture.

The application follows modern software engineering practices including:

- Separation of concerns
- Layered architecture
- Repository pattern
- Cloud-native document storage
- Event-driven processing

---

# 3. System Architecture

## 3.1 High-Level Architecture

```text
┌───────────────────┐
│ React Frontend    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ FastAPI Backend   │
└───────┬───────────┘
        │
        ├────────► PostgreSQL
        │
        ▼
     Amazon S3
        │
        ▼
   AWS Lambda
        │
        ▼
Processed Files
```

---

## 3.2 Architectural Style

The system follows a layered architecture:

```text
Request
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
Database
```

Each layer has its own responsibility and depends only on the layer beneath it.

---

# 4. Frontend Design

## 4.1 Frontend Technology

The frontend is implemented with:

- React
- React Router
- Bootstrap 5

---

## 4.2 Component Structure

```text
src/

├── pages/
│   ├── LoginPage
│   ├── RegisterPage
│   ├── ProjectsPage
│   └── ProjectDetailsPage
│
├── components/
│   ├── modals/
|   │   ├── CreateProjectModal
|   │   ├── EditProjectModal
|   │   ├── InviteMemberModal
|   │   ├── UploadDocumentModal
|   │   └── DeleteProjectModal
|   │   ├── DeleteDocumentModal
|   │   └── EditDocumentModal
|   │
│   └── projects/
|       ├── ProjectDocumentsSection
|       ├── ProjectMembersSection
|       ├── ProjectOverviewSection
|       ├── ProjectsHeader
|       └── ProjectsList
|
└── hooks/
    ├── useProjectDetails
    └── useProjects

```

---

## 4.3 Frontend Responsibilities

The frontend is responsible for:

- User interaction
- Form validation
- Sending API requests
- Managing JWT tokens
- Rendering project and document data

Business rules remain in the backend.

---

# 5. Backend Design

## 5.1 Backend Technology

The backend is implemented using:

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication

---

## 5.2 Layer Responsibilities

### Router Layer

Responsibilities:

- Receive HTTP requests
- Validate inputs
- Inject dependencies
- Return responses

Example:

```python
@router.post("/projects")
```

---

### Service Layer

Responsibilities:

- Implement business logic
- Enforce permissions
- Handle workflows
- Log business events

Example:

```python
create_project()
invite_member()
upload_document()
```

---

### Repository Layer

Responsibilities:

- Database queries
- Data persistence
- Data retrieval

Example:

```python
create_project()
get_project_by_id()
create_document()
```

---

# 6. Database Design

## 6.1 User

```text
User
-----
id
username
hashed_password
```

Purpose:

- Stores application users
- Supports authentication

---

## 6.2 Project

```text
Project
--------
id
name
description
owner_id
```

Purpose:

- Stores project metadata
- Maintains project ownership

---

## 6.3 ProjectMember

```text
ProjectMember
-------------
id
project_id
user_id
```

Purpose:

- Stores project membership
- Supports many-to-many user relationships

---

## 6.4 Document

```text
Document
--------
id
filename
s3_key
project_id
uploaded_by
```

Purpose:

- Stores document metadata
- Links documents to S3 objects

---

# 7. Authentication Design

## 7.1 Authentication Flow

```text
Login
  │
  ▼
Credential Validation
  │
  ▼
JWT Creation
  │
  ▼
JWT Returned
  │
  ▼
Stored in Browser
```

---

## 7.2 Protected Endpoints

Protected endpoints require:

```http
Authorization: Bearer <token>
```

A middleware dependency validates the JWT and resolves the current user.

---

# 8. Authorization Rules

## Project Owner

Allowed actions:

- Create project
- Update project
- Delete project
- Invite participants
- Upload documents
- Replace documents
- Delete documents

---

## Participant

Allowed actions:

- View project
- View members
- Download documents
- Upload documents

Restricted actions:

- Delete project
- Edit project
- Invite members

---

# 9. Document Management Design

## 9.1 Upload Workflow

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI
 │
 ▼
Amazon S3
 │
 ▼
Document Metadata Stored
```

---

## 9.2 Download Workflow

```text
User
 │
 ▼
FastAPI
 │
 ▼
S3 Access
 │
 ▼
Document Returned
```

---

## 9.3 Delete Workflow

```text
User
 │
 ▼
FastAPI
 │
 ▼
Delete Object From S3
 │
 ▼
Delete Metadata From Database
```

---

# 10. AWS S3 Integration

## 10.1 Purpose

The local filesystem was replaced by Amazon S3 for document storage.

Benefits:

- Scalability
- High durability
- Cloud-native storage
- Easy integration with Lambda

---

## 10.2 Storage Structure

Example:

```text
projects/

└── 1/
    ├── report.pdf
    ├── image.png
    └── specification.docx
```

Stored as:

```text
projects/1/uuid_filename.ext
```

---

# 11. AWS Lambda Design

## 11.1 Purpose

AWS Lambda automatically processes uploaded documents.

Execution is event-driven.

---

## 11.2 Trigger

```text
S3 Object Created
```

Whenever a file is uploaded:

```text
projects/...
```

the Lambda function runs automatically.

---

## 11.3 Processing Workflow

```text
Upload Document
       │
       ▼
Amazon S3
       │
       ▼
S3 Event
       │
       ▼
AWS Lambda
       │
       ▼
Create Processed Copy
```

---

## 11.4 Output

Example:

Original:

```text
projects/1/report.pdf
```

Generated automatically:

```text
processed/projects/1/report.pdf
```

---

# 12. Logging Design

## 12.1 Purpose

Logging provides traceability and supports troubleshooting.

---

## 12.2 Logged Events

### Authentication

```text
Successful login
Failed login
User registration
```

### Projects

```text
Project creation
Project modification
Project deletion
```

### Members

```text
Member invitation
```

### Documents

```text
Upload
Download
Delete
Replace
```

---

## 12.3 Logging Levels

### INFO

Business events

Example:

```text
Project created
```

### WARNING

Suspicious operations

Example:

```text
Unauthorized access
```

### ERROR

Application failures

Example:

```text
Database errors
```

---

# 13. Dockerization

## Docker Components

### Application Container

```text
FastAPI
```

### Database Container

```text
PostgreSQL
```

Managed through:

```yaml
docker-compose.yml
```

---

# 14. Security Design

Implemented security features:

- Password hashing
- JWT authentication
- Protected endpoints
- Ownership validation
- Membership validation
- AWS credential isolation through environment variables

---

# 15. Future Improvements

Potential future enhancements:

- GitHub Actions CI/CD
- AWS EC2 deployment
- Docker Registry integration
- Thumbnail generation using Pillow
- Document version history
- Notifications
- Audit logs
- Role management

---

# 16. Conclusion

The Project Management Software demonstrates the implementation of a modern cloud-enabled web application using:

- React
- FastAPI
- PostgreSQL
- Docker
- Amazon S3
- AWS Lambda

The system combines traditional CRUD functionality with cloud-native event-driven processing and scalable document storage, providing a practical example of a modern full-stack application architecture.
