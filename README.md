# AI-Powered Smart University Complaint Management and Resolution System

## Project Overview

The AI-Powered Smart University Complaint Management and Resolution System is a web-based application designed to help students submit complaints and allow university administrators and officers to manage and resolve them.

The system provides complaint tracking, staff dashboards, complaint assignment, and complaint status management.

## Technologies Used

- **Frontend:** React, Vite, JavaScript
- **Backend:** Python, FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Password Security:** bcrypt

## Main Features

- Public complaint submission without student login.
- Complaint tracking using a complaint ID.
- Image upload with complaint submission.
- Admin and officer login.
- Admin dashboard for complaint management.
- Officer dashboard for assigned complaints.
- Department and officer management.
- Complaint assignment to officers.
- Complaint status tracking and history.
- Student verification of complaint resolution.

## Project Structure

```text
UniversityComplaintSystem/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── auth.py
│   ├── database.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
│
├── database/
│   └── schema.sql
│
├── requirements.txt
└── README.md
```

## Requirements

Install the following before running the project:

- Python
- Node.js and npm
- MySQL Server
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jashmine0612/UniversityComplaintSystem.git
cd UniversityComplaintSystem
```

### 2. Create the MySQL Database

Open MySQL Workbench and run the SQL script:

```text
database/schema.sql
```

Alternatively, from the project root, run:

```bash
Get-Content .\database\schema.sql | mysql -u root -p
```

Enter your MySQL password when prompted.

### 3. Configure the Backend

Open the backend folder:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the project dependencies from the root requirements file:

```bash
pip install -r ..\requirements.txt
```

Configure the backend database connection using your local MySQL credentials and the database name:

```text
university_complaints
```

Use the environment variable names expected by the backend configuration. Do not upload database passwords or secret keys to GitHub.

### 4. Start the Backend

From the `backend` directory, run:

```bash
python -m uvicorn main:app --reload
```

Backend URL:

http://localhost:8000

API documentation:

http://localhost:8000/docs

### 5. Start the Frontend

Open another terminal:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

http://localhost:5173

## Complaint Status Flow

```text
PENDING
   |
   v
IN_PROGRESS
   |
   v
AWAITING_VERIFICATION
   |
   v
CLOSED
```

The student can confirm resolution through the complaint tracking page using the verification token.

## Important Notes

- Students do not need an account to submit or track complaints.
- Admin and officer accounts are stored in the MySQL database.
- Each team member should configure their own local database credentials.
- The schema file creates the database tables; it does not automatically create admin or officer accounts.
- Never commit passwords, API secrets, JWT keys, or private verification tokens.

## Repository

GitHub: https://github.com/jashmine0612/UniversityComplaintSystem
