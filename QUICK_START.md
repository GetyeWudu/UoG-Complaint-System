# Quick Start Guide - UoG Complaint System

Get the system running in 5 minutes!

---

## 🚀 Fastest Way to Start

### Windows (Automated)

```bash
cd backend
setup_and_run.bat
```

This script will:
1. Create virtual environment
2. Install all dependencies
3. Create .env file
4. Run migrations
5. Seed test data
6. Start the server

**That's it!** The backend will be running at http://127.0.0.1:8000

---

## 📋 Manual Setup (All Platforms)

### Step 1: Backend Setup (5 minutes)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

python manage.py makemigrations
python manage.py migrate
python manage.py seed_data

# Start server
python manage.py runserver
```

### Step 2: Test the Backend

Open your browser and visit:
- **API Docs:** http://127.0.0.1:8000/api/docs/
- **Admin Panel:** http://127.0.0.1:8000/admin/

Login with any test account:
- **Username:** student@example.com
- **Password:** Student123!

---

## 🧪 Quick API Test

### Test Login (using curl)

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"student@example.com\",\"password\":\"Student123!\"}"
```

You should get a response with a token!

### Test in Swagger UI (Easier)

1. Go to http://127.0.0.1:8000/api/docs/
2. Click on "POST /api/auth/login/"
3. Click "Try it out"
4. Enter credentials:
   ```json
   {
     "username": "student@example.com",
     "password": "Student123!"
   }
   ```
5. Click "Execute"
6. Copy the token from the response
7. Click "Authorize" button at the top
8. Enter: `Token <your-token-here>`
9. Now you can test all endpoints!

---

## 📱 Test Accounts

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

---

## ✅ Verify Everything Works

### 1. Test Login
- Go to http://127.0.0.1:8000/api/docs/
- Try logging in with student@example.com / Student123!
- ✅ Should get a token

### 2. Test Complaint Creation
- In Swagger UI, authorize with your token
- Try POST /api/complaints/
- Create a test complaint
- ✅ Should get tracking ID

### 3. Test File Upload
- Create a complaint first
- Try POST /api/complaints/{id}/files/
- Upload a test image
- ✅ Should upload successfully

### 4. Test Admin Panel
- Go to http://127.0.0.1:8000/admin/
- Login with super@example.com / Super123!
- ✅ Should see Django admin interface

### 5. Check Email Notifications
- Look at your terminal/console
- When you create a complaint, you should see email output
- ✅ Email should be printed to console

---

## 🐛 Common Issues

### "No module named 'django'"
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### "Port already in use"
```bash
# Use a different port
python manage.py runserver 8001
```

### "Migration errors"
```bash
# Delete database and start fresh
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🎯 What to Test

### As Student
1. Login
2. Create complaint
3. Upload files
4. Add comments
5. Submit feedback

### As Staff
1. Login
2. View assigned complaints
3. Update status
4. Add comments

### As Admin
1. Login
2. View all complaints
3. Assign complaints
4. Manage users in admin panel

---

## 📊 Run Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test
pytest tests/test_auth.py -v
```

---

## 🎉 Success Checklist

- [ ] Backend server running on port 8000
- [ ] Can access Swagger UI
- [ ] Can login with test accounts
- [ ] Can create complaints
- [ ] Can upload files
- [ ] Can access admin panel
- [ ] Tests pass

If all checks pass, **you're ready!** ✅

---

## 📚 Next Steps

1. **Explore the API** - http://127.0.0.1:8000/api/docs/
2. **Read the docs** - Check README.md and other documentation
3. **Run tests** - `pytest` to verify everything works
4. **Start frontend** - Move to frontend development

---

## 💡 Pro Tips

1. **Use Swagger UI** for testing - it's much easier than curl
2. **Check console** for email output during development
3. **Use Django admin** to view/edit data directly
4. **Run tests** before making changes
5. **Check activity logs** in admin panel to debug auth issues

---

**Need help?** Check the detailed documentation:
- [Setup Guide](SETUP.md)
- [API Reference](API_QUICK_REFERENCE.md)
- [Next Steps](NEXT_STEPS.md)

---

**Ready to code!** 🚀
