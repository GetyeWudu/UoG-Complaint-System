# UoG Complaint Management System - Setup Guide

This guide will help you set up the project locally for development and testing.

---

## Prerequisites

- **Python 3.10+** (for Django backend)
- **Node.js 18+** and npm (for React frontend)
- **Git** (for version control)
- **SQLite** (comes with Python)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/GetyeWudu/UoG-Complaint-System.git
cd UoG-Complaint-System
git checkout feature/complete-final-project
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from example)
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed database with test data
python manage.py seed_data

# Create logs directory
mkdir logs

# Run development server
python manage.py runserver
```

Backend will be available at: http://127.0.0.1:8000

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## Test Accounts

After running `python manage.py seed_data`, you can login with these accounts:

| Email | Password | Role |
|-------|----------|------|
| student@example.com | Student123! | Student |
| staff@example.com | Staff123! | Academic Staff |
| nonstaff@example.com | NonStaff123! | Non-academic Staff |
| maint@example.com | Maint123! | Maintenance Worker |
| depthead@example.com | DeptHead123! | Department Head |
| admin@example.com | Admin123! | System Admin |
| super@example.com | Super123! | Super Admin |

---

## Environment Variables

Key environment variables in `backend/.env`:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (for testing, use Mailtrap)
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your-mailtrap-username
EMAIL_HOST_PASSWORD=your-mailtrap-password

# OAuth (optional, for university SSO)
OAUTH_ENABLED=False
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
```

---

## API Documentation

Once the backend is running, access API documentation at:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **ReDoc:** http://127.0.0.1:8000/api/redoc/

---

## Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## Common Issues

### Issue: "No module named 'decouple'"
**Solution:** Make sure you've activated the virtual environment and installed requirements:
```bash
pip install -r requirements.txt
```

### Issue: "CORS error" in frontend
**Solution:** Check that backend is running on port 8000 and frontend on port 5173. Update CORS_ALLOWED_ORIGINS in .env if needed.

### Issue: "Database is locked"
**Solution:** Close any other processes accessing the database, or delete db.sqlite3 and run migrations again.

### Issue: Email not sending
**Solution:** For local development, emails will print to console by default. To test real emails, sign up for a free Mailtrap account and update EMAIL_* settings in .env.

---

## Project Structure

```
UoG-Complaint-System/
├── backend/
│   ├── accounts/          # User management
│   ├── complaints/        # Complaint system
│   ├── config/           # Django settings
│   ├── media/            # Uploaded files
│   ├── logs/             # Application logs
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   └── api.js
│   ├── package.json
│   └── vite.config.js
├── audit.md
├── ROADMAP.md
├── CHECKLIST.md
├── PROGRESS.md
└── README.md
```

---

## Next Steps

1. ✅ Complete backend authentication endpoints
2. ✅ Implement file upload system
3. ✅ Build complaint workflow
4. ✅ Add email notifications
5. ✅ Create frontend dashboards
6. ✅ Implement analytics
7. ✅ Write tests
8. ✅ Generate documentation

---

## Support

For issues or questions:
- Check [PROGRESS.md](./PROGRESS.md) for current status
- Review [audit.md](./audit.md) for technical details
- See [ROADMAP.md](./ROADMAP.md) for planned features

---

**Happy Coding! 🚀**
