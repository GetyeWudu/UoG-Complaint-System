# 🎯 Complete Testing Guide - Email Notifications

## 📋 Quick Answer to Your Questions

### Q1: "Where is the button to change complaint status?"
**A:** The "Update Status" button is on the **Complaint Detail page**, top-right corner, **only visible to admins**.

### Q2: "How do I test real email notifications?"
**A:** Configure Gmail in `backend/.env` and change complaint status. See detailed steps below.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 2: Login as Admin

Go to: http://localhost:5173/login

```
Email: admin@uog.edu.et
Password: password123
```

### Step 3: Open Any Complaint

- Click on any complaint from the dashboard
- Look at **top-right corner**
- You'll see a blue **"Update Status"** button

### Step 4: Change Status

- Click "Update Status"
- Select "Assigned"
- Click "Update & Send Email"

### Step 5: Check Email

**Console Mode (Current Setup):**
- Look at your backend terminal
- You'll see the email printed there!

**Real Email Mode:**
- Configure Gmail (see below)
- Check your inbox

---

## 📧 Email Testing - Two Modes

### Mode 1: Console (Already Working) ✅

**Current Configuration:**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**What Happens:**
- Emails print to backend terminal/console
- No actual emails sent
- Perfect for development testing

**How to Test:**
1. Start backend: `python manage.py runserver`
2. Change complaint status (as admin)
3. Check backend terminal - you'll see:

```
Content-Type: text/plain; charset="utf-8"
Subject: Your Complaint Has Been Assigned - CMP-ABC123
From: UoG Complaints <noreply@uog.edu.et>
To: student@uog.edu.et

Dear Student Name,

Your complaint has been assigned to a staff member...
```

---

### Mode 2: Real Gmail (Production) 📨

#### Step 1: Get Gmail App Password

1. **Enable 2-Step Verification:**
   - Go to: https://myaccount.google.com/security
   - Turn on "2-Step Verification"

2. **Create App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - **Copy the 16-character password**
   - Example: `abcd efgh ijkl mnop`

#### Step 2: Edit backend/.env

Open `backend/.env` and change:

```env
# Comment out console backend
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Add real email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=UoG Complaints <your-email@gmail.com>
```

**Replace:**
- `your-email@gmail.com` → Your actual Gmail
- `abcdefghijklmnop` → Your 16-char app password (no spaces!)

#### Step 3: Restart Backend

```bash
# Stop backend (Ctrl+C)
# Start again
cd backend
python manage.py runserver
```

#### Step 4: Test with Your Email

1. **Register with your real email:**
   - Go to: http://localhost:5173/register
   - Use your actual email address
   - Complete registration

2. **Create a complaint** (as that student)

3. **Login as admin** and change status

4. **Check your email inbox!** 📬

---

## 🎬 Complete Testing Workflow

### Test All 6 Email Types

#### Preparation:
```bash
# Make sure test accounts exist
cd backend
python manage.py seed_data
```

This creates:
- **Student:** student@uog.edu.et / password123
- **Admin:** admin@uog.edu.et / password123

---

#### Test 1: NEW → ASSIGNED

**As Student:**
1. Login: student@uog.edu.et / password123
2. Create complaint: "Broken projector in Room 301"
3. Submit and note tracking ID

**As Admin:**
1. Logout and login: admin@uog.edu.et / password123
2. Go to Dashboard
3. Click on the complaint
4. Click "Update Status" button (top-right)
5. Select "Assigned"
6. Click "Update & Send Email"

**Check Email:**
```
Subject: Your Complaint Has Been Assigned - CMP-XXX
Content: "Your complaint has been assigned to a staff member..."
```

---

#### Test 2: ASSIGNED → IN_PROGRESS

**As Admin:**
1. Open same complaint
2. Click "Update Status"
3. Select "In Progress"
4. Click "Update & Send Email"

**Check Email:**
```
Subject: Your Complaint is Being Processed - CMP-XXX
Content: "Your complaint is now being actively worked on..."
```

---

#### Test 3: IN_PROGRESS → RESOLVED

**As Admin:**
1. Open same complaint
2. Click "Update Status"
3. Select "Resolved"
4. **Enter resolution notes:** "Projector replaced. Tested and working."
5. Click "Update & Send Email"

**Check Email:**
```
Subject: Your Complaint Has Been Resolved - CMP-XXX
Content: "Great news! Your complaint has been resolved."
Resolution Notes: "Projector replaced. Tested and working."
```

---

#### Test 4: Test REJECTED Status

**As Student:**
1. Create another complaint: "Duplicate issue"

**As Admin:**
1. Open the new complaint
2. Click "Update Status"
3. Select "Rejected"
4. **Enter rejection reason:** "Duplicate complaint. See CMP-001"
5. Click "Update & Send Email"

**Check Email:**
```
Subject: Your Complaint Cannot Be Processed - CMP-XXX
Content: "Unfortunately, we cannot proceed with your complaint."
Rejection Reason: "Duplicate complaint. See CMP-001"
```

---

#### Test 5: RESOLVED → CLOSED

**As Admin:**
1. Go back to resolved complaint
2. Click "Update Status"
3. Select "Closed"
4. Click "Update & Send Email"

**Check Email:**
```
Subject: Your Complaint Has Been Closed - CMP-XXX
Content: "Your complaint has been closed."
```

---

#### Test 6: NEW → REVIEWED (Optional)

Some systems have a "reviewed" status. If you add it:

**As Admin:**
1. Open new complaint
2. Click "Update Status"
3. Select "Reviewed"
4. Click "Update & Send Email"

**Check Email:**
```
Subject: Your Complaint Has Been Reviewed - CMP-XXX
Content: "Your complaint has been reviewed by our team."
```

---

## 🔍 Where is the Update Status Button?

### Visual Location:

```
Complaint Detail Page
┌─────────────────────────────────────────────────┐
│ ← Back to Dashboard                             │
│                                                 │
│ ┌─────────────────────────────────────────────┐│
│ │ Broken Projector in Room 301                ││
│ │ Tracking ID: CMP-ABC123                     ││
│ │                                             ││
│ │                        ┌──────────┐        ││
│ │                        │   NEW    │        ││ ← Status Badge
│ │                        └──────────┘        ││
│ │                        ┌──────────────┐    ││
│ │                        │Update Status │    ││ ← THE BUTTON!
│ │                        └──────────────┘    ││
│ │                                             ││
│ │ Description:                                ││
│ │ The projector is not working...            ││
│ └─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

### Who Can See It?

✅ **Can see button:**
- Admin
- Super Admin
- Department Head
- Proctor

❌ **Cannot see button:**
- Student
- Guest

### Check Your Role:

Open browser console (F12) and type:
```javascript
JSON.parse(localStorage.getItem('user'))
```

Look for `"role": "admin"` or `"role": "student"`

---

## 🐛 Troubleshooting

### Problem 1: "I don't see the Update Status button"

**Solutions:**
1. ✅ Make sure you're logged in as **admin** (not student)
2. ✅ Make sure you're on the **complaint detail page** (not dashboard)
3. ✅ URL should be: `http://localhost:5173/complaints/1`
4. ✅ Refresh page (Ctrl+F5)

**Test your role:**
```javascript
// Browser console (F12)
const user = JSON.parse(localStorage.getItem('user'));
console.log('Role:', user.role);
console.log('Should see button:', ['admin', 'super_admin', 'dept_head', 'proctor'].includes(user.role));
```

---

### Problem 2: "Emails not showing in console"

**Solutions:**
1. ✅ Check `backend/.env` has:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```
2. ✅ Backend is running in terminal (not background)
3. ✅ Look at the **backend terminal** (not frontend)
4. ✅ Status was actually changed (check complaint detail page)

---

### Problem 3: "Real emails not sending"

**Solutions:**
1. ✅ Gmail 2-Step Verification is enabled
2. ✅ App password is correct (16 chars, no spaces)
3. ✅ `backend/.env` is configured correctly
4. ✅ Backend was restarted after changing `.env`
5. ✅ Check backend console for error messages

**Test email configuration:**
```bash
cd backend
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

print("Backend:", settings.EMAIL_BACKEND)
print("Host:", settings.EMAIL_HOST)
print("User:", settings.EMAIL_HOST_USER)

# Send test
send_mail(
    'Test Email',
    'This is a test',
    settings.DEFAULT_FROM_EMAIL,
    ['your-email@gmail.com'],
    fail_silently=False,
)
print("✅ Sent!")
```

---

### Problem 4: "Emails go to spam"

**Solutions:**
1. Mark as "Not Spam" in Gmail
2. Add sender to contacts
3. Check spam folder first
4. In production, use proper domain email (not Gmail)

---

## 📊 Expected Email Examples

### Email 1: Assigned
```
From: UoG Complaints <noreply@uog.edu.et>
To: student@uog.edu.et
Subject: Your Complaint Has Been Assigned - CMP-ABC123

Dear John Doe,

Your complaint has been assigned to a staff member for resolution.

Complaint Details:
- Tracking ID: CMP-ABC123
- Title: Broken projector in Room 301
- Status: Assigned
- Assigned to: Admin User

We will keep you updated on the progress.

Best regards,
UoG Complaint Management Team
```

### Email 2: In Progress
```
Subject: Your Complaint is Being Processed - CMP-ABC123

Dear John Doe,

Your complaint is now being actively worked on.

Complaint Details:
- Tracking ID: CMP-ABC123
- Title: Broken projector in Room 301
- Status: In Progress
- Assigned to: Admin User

We are working to resolve your issue as quickly as possible.

Best regards,
UoG Complaint Management Team
```

### Email 3: Resolved
```
Subject: Your Complaint Has Been Resolved - CMP-ABC123

Dear John Doe,

Great news! Your complaint has been resolved.

Complaint Details:
- Tracking ID: CMP-ABC123
- Title: Broken projector in Room 301
- Status: Resolved

Resolution Notes:
Projector has been replaced with a new one. Tested and working properly.

If you are satisfied with the resolution, no further action is needed.
If you have any concerns, please contact us.

Best regards,
UoG Complaint Management Team
```

### Email 4: Rejected
```
Subject: Your Complaint Cannot Be Processed - CMP-ABC123

Dear John Doe,

Unfortunately, we cannot proceed with your complaint at this time.

Complaint Details:
- Tracking ID: CMP-ABC123
- Title: Broken projector in Room 301
- Status: Rejected

Rejection Reason:
This is a duplicate complaint. Please refer to CMP-001 for updates.

If you have questions, please contact us.

Best regards,
UoG Complaint Management Team
```

### Email 5: Closed
```
Subject: Your Complaint Has Been Closed - CMP-ABC123

Dear John Doe,

Your complaint has been closed.

Complaint Details:
- Tracking ID: CMP-ABC123
- Title: Broken projector in Room 301
- Status: Closed

Thank you for using the UoG Complaint Management System.

Best regards,
UoG Complaint Management Team
```

---

## ✅ Testing Checklist

### Before Testing:
- [ ] Backend running (`python manage.py runserver`)
- [ ] Frontend running (`npm run dev`)
- [ ] Test accounts created (`python manage.py seed_data`)
- [ ] Email backend configured (console or Gmail)

### Console Mode Testing:
- [ ] Created complaint as student
- [ ] Logged in as admin
- [ ] Found "Update Status" button
- [ ] Changed status to "Assigned"
- [ ] Saw email in backend console
- [ ] Email has correct tracking ID
- [ ] Email has correct student name
- [ ] Tested all 6 status changes

### Real Email Testing:
- [ ] Gmail 2-Step Verification enabled
- [ ] App password generated
- [ ] `backend/.env` configured
- [ ] Backend restarted
- [ ] Registered with real email
- [ ] Created complaint
- [ ] Changed status as admin
- [ ] Received email in inbox
- [ ] Email properly formatted
- [ ] All details correct

---

## 🎯 Summary

1. **The button EXISTS** - It's on the complaint detail page, top-right corner
2. **Only admins see it** - Students don't have permission
3. **Console mode works NOW** - Check backend terminal for emails
4. **For real emails** - Configure Gmail app password in `.env`
5. **6 email types** - One for each status change
6. **Automatic** - No manual email sending needed

---

## 📞 Still Need Help?

### Quick Checks:
```bash
# 1. Check if backend is running
curl http://127.0.0.1:8000/api/complaints/

# 2. Check if frontend is running
curl http://localhost:5173/

# 3. Check email backend
cd backend
python manage.py shell -c "from django.conf import settings; print(settings.EMAIL_BACKEND)"
```

### Debug Info to Collect:
1. Screenshot of complaint detail page
2. Browser console errors (F12)
3. Backend console output
4. Your role (from localStorage)
5. Email backend setting

The system is working - you just need to find the button and configure email! 🎉
