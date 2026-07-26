# SDLC Assistant

A full-stack SDLC (Software Development Life Cycle) management platform built with **FastAPI**, **SQLite**, and a web frontend. The application helps project managers and development teams manage software projects by generating SDLC artifacts, tracking project workflow, and managing project tasks.

> 🚧 This project is actively under development and is being enhanced into a backend-focused, SQL-heavy SDLC management platform.

---

## Features

### Authentication
- User Signup
- User Login
- Session-based access using user IDs

### AI-Assisted Requirement Analysis
- Generate User Stories
- Generate Acceptance Criteria
- Generate Test Cases
- Requirement file upload support
- Editable generated artifacts
- Export artifacts as JSON
- Export artifacts as Markdown

### Project Management
- Create projects
- Store projects in SQLite database
- View previous projects
- Edit generated artifacts
- Delete projects

### SDLC Workflow Engine
- Track project lifecycle
- Workflow stages:
  - Requirement
  - Design
  - Development
  - Testing
  - Deployment
- Advance project through workflow stages
- View current workflow status

### Task Management
- Create tasks for a project
- Assign tasks to users
- Track task status
  - To Do
  - In Progress
  - Done
- View all tasks belonging to a project
- Status validation for task updates

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### AI
- Local LLM integration (currently mocked during development)

---

## Database Schema

### Users

| Column | Type |
|---------|------|
| id | Integer |
| username | Text |
| password | Text |

---

### Projects

| Column | Type |
|---------|------|
| id | Integer |
| requirement | Text |
| user_stories | Text |
| acceptance_criteria | Text |
| test_cases | Text |
| current_stage | Text |
| user_id | Integer |

---

### Tasks

| Column | Type |
|---------|------|
| id | Integer |
| title | Text |
| description | Text |
| status | Text |
| project_id | Integer |
| assigned_to | Integer |

---

## Current API Endpoints

### Authentication

```
POST /signup
POST /login
```

### Project APIs

```
POST   /generate
GET    /projects/{id}
PUT    /projects/{id}
DELETE /projects/{id}
GET    /projects/user/{user_id}
```

### Workflow APIs

```
POST /project/{project_id}/advance
GET  /projects/{project_id}/workflow
```

### Task APIs

```
POST /tasks/create
GET  /projects/{project_id}/tasks
PUT  /tasks/{task_id}/status
```

---

## Project Structure

```
backend/
│
├── main.py
├── models.py
├── database.py
└── ...

frontend/
│
├── index.html
├── script.js
└── style.css
```

---

## Deployment

Frontend is deployed using Netlify.

Backend is deployed using Render.

---

## Roadmap

Upcoming enhancements include:

- JWT Authentication
- Role-Based Access Control
- Team Management
- Workflow Validation Rules
- Activity Logs
- Task Comments
- Docker Support
- GitHub Actions CI/CD
- PostgreSQL Migration
- AI-powered API Suggestions
- SaaS Billing (Mock Razorpay)
- Responsive Dashboard
- Architecture Documentation

---

## Author

**Ananya Samudrala**

Computer Science Engineering Student

Backend • System Design • Full Stack Development
