# Running the Backend - Step by Step

Follow these steps to get the backend running:

## Step 1: Install Dependencies

```bash
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Open .env and configure (optional for now, defaults work):
# - SECRET_KEY (can leave default for development)
# - EMAIL_BACKEND (default is console, which prints emails to terminal)
# - Other settings as needed
```

## Step 3: Create Database

```bash
# Create migrations
python manage.py makemigrations accounts
python manage.py makemigrations complaints

# Apply migrations
python manage.py migrate

# Create logs directory
mkdir logs
```

## Step 4: Load Test Data

```bash
# Seed database with test accounts and data
python manage.py seed_data
```

This will create:
- 3 Campuses (Tewodros, Maraki, CMHS)
- 2 Colleges
- 4 Departments
- 7 Test user accounts
- 5 Categories with subcategories
- Email templates
- Routing rules

## Step 5: Create Superuser (Optional)

```bash
# Create Django admin superuser
python manage.py createsuperuser

# Follow prompts to create admin account
```

## Step 6: Run Server

```bash
# Start development server
python manage.py runserver
```

Server will start at: **http://127.0.0.1:8000**

## Step 7: Test the API

### Option 1: Use Swagger UI (Recommended)
Visit: **http://127.0.0.1:8000/api/docs/**

This provides an interactive interface to test all endpoints.

### Option 2: Use curl

```bash
# Test login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"student@example.com\",\"password\":\"Student123!\"}"

# You should get a response with a token
```

### Option 3: Use Django Admin
Visit: **http://127.0.0.1:8000/admin/**

Login with superuser credentials (if created) or use:
- Username: super@example.com
- Password: Super123!

## Test Accounts

| Email | Password | Role |
|-------|----------|------|
| student@example.com | Student123! | Student |
| staff@example.com | Staff123! | Academic Staff |
| nonstaff@example.com | NonStaff123! | Non-academic Staff |
| maint@example.com | Maint123! | Maintenance Worker |
| depthead@example.com | DeptHead123! | Department Head |
| admin@example.com | Admin123! | System Admin |
| super@example.com | Super123! | Super Admin |

## Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Make sure virtual environment is activated
```bash
venv\Scripts\activate  # Windows
```

### Issue: "No module named 'decouple'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Migration errors
**Solution:** Delete database and start fresh
```bash
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### Issue: "Port already in use"
**Solution:** Use a different port
```bash
python manage.py runserver 8001
```

### Issue: CORS errors (when testing with frontend)
**Solution:** Check .env file has correct CORS settings
```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_auth.py
```

## Next Steps

Once backend is running successfully:
1. ✅ Test API endpoints in Swagger UI
2. ✅ Verify test accounts work
3. ✅ Check Django admin panel
4. ✅ Test file uploads
5. ✅ Verify email notifications (check console)
6. ➡️ Move to frontend development

## Quick Verification Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Migrations applied
- [ ] Seed data loaded
- [ ] Server running on port 8000
- [ ] Swagger UI accessible
- [ ] Can login with test accounts
- [ ] Django admin accessible

If all checks pass, you're ready to proceed! ✅
