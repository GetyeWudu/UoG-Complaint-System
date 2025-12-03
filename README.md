# University of Gondar (UoG) Complaint Management System

A comprehensive web-based complaint management system for University of Gondar, featuring AI-powered chatbot assistance, multi-language support, and role-based dashboards.

## Overview

This system streamlines the complaint handling process at UoG by providing:
- Automated complaint submission and tracking
- AI-powered chatbot for instant university information
- Role-based dashboards (Student, Staff, Dean, Admin)
- Email notifications and SLA tracking
- Multi-language support (English & Amharic)
- Public complaint tracking without login

## Technology Stack

### Backend
- Django 5.2.8 (Python web framework)
- Django REST Framework (API)
- SQLite (Development database)
- Groq AI / Google Gemini (AI chatbot)
- SMTP Email integration

### Frontend
- React 18.3.1
- Vite (Build tool)
- React Router (Navigation)
- Axios (HTTP client)
- i18next (Internationalization)

## Key Features

### 1. Complaint Management
- Submit complaints with file attachments
- Track complaint status in real-time
- Automated tracking ID generation (CMP-XXXXXXXX)
- SLA (Service Level Agreement) monitoring
- Status workflow: New → Assigned → In Progress → Resolved → Closed

### 2. AI Chatbot Assistant
- Powered by Groq AI (Llama 3.3 70B model)
- Fallback to Google Gemini API
- Comprehensive UoG knowledge base
- Answers questions about:
  - University information and history
  - Colleges and departments
  - Admission procedures
  - Fees and scholarships
  - Library services
  - Course registration
  - Campus facilities
- Multi-language support (English/Amharic)

### 3. Role-Based Dashboards

**Student Dashboard:**
- Submit new complaints
- View complaint history
- Track complaint status
- Access AI chatbot

**Staff Dashboard:**
- View assigned complaints
- Update complaint status
- Add internal notes
- Assign complaints to other staff

**Dean Dashboard:**
- Monitor college-specific complaints
- Review complaint statistics
- Approve resolutions

**Admin Dashboard:**
- System-wide complaint overview
- User management
- Analytics and reporting
- System configuration

### 4. Email Notifications
- Complaint submission confirmation
- Status update notifications
- Assignment notifications
- Resolution notifications
- Configurable SMTP settings

### 5. Multi-Language Support
- English (default)
- Amharic (አማርኛ)
- Language switcher in UI
- Translated complaint forms and dashboards

## Installation & Setup

### Prerequisites
- Python 3.10+ (Note: Python 3.14 may have compatibility issues)
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy .env.example to .env and update:
# - GROQ_API_KEY (get from https://console.groq.com/)
# - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
# - SECRET_KEY

# Run migrations
python manage.py migrate

# Create test users
python manage.py seed_test_users

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Test Credentials

After running `seed_test_users`, you can login with:

**Admin:**
- Email: admin@uog.edu.et
- Password: admin123

**Student:**
- Email: student@uog.edu.et
- Password: student123

**Staff:**
- Email: staff@example.com
- Password: staff123

**Dean:**
- Email: dean@example.com
- Password: dean123

## API Endpoints

### Authentication
- POST `/api/auth/login/` - User login
- POST `/api/auth/logout/` - User logout
- GET `/api/auth/me/` - Get current user

### Complaints
- GET `/api/complaints/` - List complaints
- POST `/api/complaints/` - Create complaint
- GET `/api/complaints/{id}/` - Get complaint details
- PATCH `/api/complaints/{id}/` - Update complaint
- GET `/api/public/track/{tracking_id}/` - Public tracking

### Chatbot
- POST `/api/complaints/chatbot/message/` - Send message to chatbot
- GET `/api/complaints/chatbot/suggestions/` - Get suggested questions

### Dashboards
- GET `/api/complaints/dashboards/student/stats/` - Student statistics
- GET `/api/complaints/dashboards/admin/stats/` - Admin statistics

## AI Chatbot Configuration

The system supports two AI providers:

### Groq AI (Recommended)
- Fast and generous rate limits (6000 requests/minute)
- Free tier available
- Get API key: https://console.groq.com/
- Set in .env: `GROQ_API_KEY=gsk_...`

### Google Gemini (Fallback)
- Free tier: 15 requests/minute
- Get API key: https://console.cloud.google.com/
- Set in .env: `GEMINI_API_KEY=AIza...`

The system automatically uses Groq if available, falling back to Gemini if needed.

## Project Structure

```
.
├── backend/
│   ├── accounts/          # User authentication & management
│   ├── complaints/        # Complaint handling & chatbot
│   ├── config/           # Django settings
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── context/      # React context (auth, language)
│   │   └── i18n/         # Translation files
│   └── package.json
└── README.md
```

## Development

### Adding New Features
1. Backend: Create/modify Django apps in `backend/`
2. Frontend: Add components in `frontend/src/`
3. Update API endpoints in `backend/complaints/urls.py`
4. Add translations in `frontend/src/i18n/locales/`

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## Deployment

### Backend (Django)
1. Set `DEBUG=False` in .env
2. Configure production database (PostgreSQL recommended)
3. Set proper `ALLOWED_HOSTS`
4. Use production WSGI server (Gunicorn/uWSGI)
5. Configure static files serving

### Frontend (React)
1. Build production bundle: `npm run build`
2. Serve `dist/` folder with Nginx/Apache
3. Configure API proxy if needed

## Troubleshooting

### Groq API Issues
- Verify API key is correct
- Check rate limits (6000/min free tier)
- Test with: `python backend/test_groq_rest.py`

### Email Not Sending
- Verify SMTP credentials in .env
- Check EMAIL_HOST and EMAIL_PORT
- For Gmail, use App Password (not regular password)

### Database Issues
- Delete `db.sqlite3` and run migrations again
- Run: `python manage.py migrate --run-syncdb`

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is developed for University of Gondar.

## Support

For issues or questions:
- Email: support@uog.edu.et
- Create an issue in the repository

## Acknowledgments

- University of Gondar IT Department
- Groq AI for providing free AI API access
- Google Gemini for AI capabilities
- Open source community

---

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Status:** Production Ready
