# Next Steps - UoG Complaint Management System

## ✅ What's Been Completed

### Phase 0 (100%)
- Comprehensive repository audit
- Development roadmap (19 days)
- Acceptance checklist
- Project documentation

### Phase 1 (60%)
- ✅ Dependencies & configuration
- ✅ Database schema refactoring (11 new models)
- ✅ Authentication system (registration, login, password reset, OAuth scaffold)
- ✅ Seed data script
- ⏳ File upload system (TODO)
- ⏳ Complaint workflow (TODO)
- ⏳ Email notifications (TODO)
- ⏳ Testing (TODO)

---

## 🚀 Immediate Next Steps

### Step 1: Install Dependencies & Setup Database

```bash
# Navigate to backend
cd backend

# Windows:
install_dependencies.bat

# Linux/Mac:
chmod +x install_dependencies.sh
./install_dependencies.sh

# Or manually:
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env file and configure:
# - SECRET_KEY (generate a new one)
# - EMAIL settings (use Mailtrap for testing)
# - Other settings as needed
```

### Step 3: Create Database & Run Migrations

```bash
# Create migrations
python manage.py makemigrations accounts
python manage.py makemigrations complaints

# Apply migrations
python manage.py migrate

# Create logs directory
mkdir logs  # Windows
mkdir -p logs  # Linux/Mac
```

### Step 4: Seed Test Data

```bash
# Populate database with test data
python manage.py seed_data

# This creates:
# - 3 campuses (Tewodros, Maraki, CMHS)
# - 2 colleges (CoI, CNCS)
# - 4 departments
# - 7 test user accounts
# - 5 categories with subcategories
# - Email templates
# - Routing rules
```

### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run Backend Server

```bash
python manage.py runserver

# Backend will be available at:
# http://127.0.0.1:8000

# API Documentation:
# http://127.0.0.1:8000/api/docs/
```

### Step 7: Setup Frontend

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend will be available at:
# http://localhost:5173
```

---

## 🧪 Test the Authentication System

### Test Accounts
All passwords follow the format: `RoleName123!`

| Email | Password | Role |
|-------|----------|------|
| student@example.com | Student123! | Student |
| staff@example.com | Staff123! | Academic Staff |
| nonstaff@example.com | NonStaff123! | Non-academic Staff |
| maint@example.com | Maint123! | Maintenance Worker |
| depthead@example.com | DeptHead123! | Department Head |
| admin@example.com | Admin123! | System Admin |
| super@example.com | Super123! | Super Admin |

### Test Registration

```bash
# Using curl
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "first_name": "Test",
    "last_name": "User",
    "role": "student"
  }'
```

### Test Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student@example.com",
    "password": "Student123!"
  }'

# Response will include token:
# {
#   "token": "abc123...",
#   "user_id": 1,
#   "username": "student@example.com",
#   "role": "student",
#   ...
# }
```

### Test Password Reset

```bash
# Request reset
curl -X POST http://127.0.0.1:8000/api/auth/password-reset/request/ \
  -H "Content-Type: application/json" \
  -d '{"email": "student@example.com"}'

# Check console for reset token (or email if SMTP configured)

# Confirm reset
curl -X POST http://127.0.0.1:8000/api/auth/password-reset/confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your-token-here",
    "password": "NewPass123!",
    "password_confirm": "NewPass123!"
  }'
```

### Test API Documentation

Visit http://127.0.0.1:8000/api/docs/ to see interactive API documentation with all endpoints.

---

## 📋 Remaining Tasks in Phase 1

### Milestone 1.4: File Upload System (Next Priority)
- [ ] Implement server-side file validation (type, size)
- [ ] Create ComplaintFile CRUD endpoints
- [ ] Implement authenticated file serving
- [ ] Support multiple file uploads per complaint
- [ ] Add file deletion with permission checks
- [ ] Update complaint serializers to include files

**Estimated Time:** 1 day

### Milestone 1.5: Complaint Workflow & Assignment
- [ ] Implement auto-routing based on RoutingRule
- [ ] Create assignment endpoints (assign to staff)
- [ ] Implement status transition validation
- [ ] Create approval workflow (Dept Head approval)
- [ ] Add comment/messaging endpoints
- [ ] Implement notification triggers
- [ ] Create ComplaintEvent on all actions
- [ ] Add permission checks for all operations

**Estimated Time:** 2 days

### Milestone 1.6: Email Notifications
- [ ] Enhance email service layer
- [ ] Create remaining email templates in database
- [ ] Add email sending on complaint submission
- [ ] Add email on assignment
- [ ] Add email on status change
- [ ] Add email on resolution
- [ ] Test with local SMTP (Mailtrap)

**Estimated Time:** 1 day

### Milestone 1.7: Testing
- [ ] Unit tests for models
- [ ] Unit tests for serializers
- [ ] Integration tests for auth endpoints
- [ ] Integration tests for complaint endpoints
- [ ] Test coverage > 70%

**Estimated Time:** 1 day

---

## 🎯 Success Criteria for Phase 1

- [x] All dependencies installed
- [x] Database schema complete with 11 models
- [x] Authentication system working (register, login, password reset)
- [x] Activity logging functional
- [x] Seed data script working
- [ ] File upload system with validation
- [ ] Complaint workflow with auto-routing
- [ ] Email notifications working
- [ ] Test coverage > 70%
- [ ] API documentation accessible

---

## 🐛 Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Activate virtual environment first
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Issue: "No module named 'decouple'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Migration errors
**Solution:** Delete db.sqlite3 and migrations, start fresh
```bash
# Delete database
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

# Delete migration files (keep __init__.py)
# Then run makemigrations and migrate again
```

### Issue: "CORS error" in frontend
**Solution:** Check CORS_ALLOWED_ORIGINS in .env includes http://localhost:5173

### Issue: Emails not sending
**Solution:** Check EMAIL_BACKEND in .env. For development, use console backend:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 📚 Documentation Links

- [Audit Report](./audit.md) - Technical analysis
- [Roadmap](./ROADMAP.md) - Full development plan
- [Progress](./PROGRESS.md) - Current status
- [Checklist](./CHECKLIST.md) - Acceptance criteria
- [Setup Guide](./SETUP.md) - Quick start guide

---

## 💡 Tips

1. **Use API Documentation:** Visit /api/docs/ to test endpoints interactively
2. **Check Activity Logs:** Login as admin and visit /api/auth/activity-logs/ to see all system events
3. **Use Django Admin:** Visit /admin/ to manage data through Django's admin interface
4. **Test with Postman:** Import the API schema from /api/schema/ into Postman for easier testing
5. **Monitor Console:** Watch the console for email output and debug information

---

**Current Status:** Phase 1 - 60% Complete  
**Next Milestone:** File Upload System (Milestone 1.4)  
**Estimated Completion:** December 16, 2025
