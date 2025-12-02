# 🧪 Testing Email Notifications - Complete Guide

## ✅ Good News: The Status Update Button Already Exists!

The "Update Status" button is **already implemented** in your ComplaintDetail page. Here's where to find it:

### 📍 Where is the Button?

1. **Login as Admin** (role: admin, super_admin, dept_head, or proctor)
2. **Go to Dashboard** - You'll see all complaints
3. **Click on any complaint** - Opens the ComplaintDetail page
4. **Look at the top-right corner** - You'll see:
   - Status badge (e.g., "NEW", "ASSIGNED", etc.)
   - **"Update Status" button** (blue button below the status badge)

### 🎯 The Button Only Shows for Admins

If you don't see the button, check:
- ✅ Are you logged in as admin/super_admin/dept_head/proctor?
- ✅ Are you on the complaint detail page (not the dashboard)?
- ✅ Is the frontend running properly?

---

## 📧 How to Test Email Notifications

### Option 1: Console Mode (Quick Testing - Already Configured)

**Current Setup:** Your system is already configured to print emails to the console.

#### Steps:

1. **Make sure backend is running:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Create a test complaint as a student:**
   - Login as student (email: student@uog.edu.et)
   - Create a new complaint
   - Note the tracking ID

3. **Change status as admin:**
   - Login as admin (email: admin@uog.edu.et)
   - Click on the complaint
   - Click "Update Status" button
   - Select "Assigned" → Click "Update & Send Email"

4. **Check the backend console/terminal:**
   You'll see the email printed like this:
   ```
   Content-Type: text/plain; charset="utf-8"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   Subject: Your Complaint Has Been Assigned - CMP-ABC123
   From: UoG Complaints <noreply@uog.edu.et>
   To: student@uog.edu.et
   Date: Fri, 28 Nov 2025 10:30:00 -0000
   Message-ID: <...>

   Dear Student Name,

   Your complaint has been assigned to a staff member for resolution.

   Complaint Details:
   - Tracking ID: CMP-ABC123
   - Title: Your complaint title
   - Status: Assigned
   - Assigned to: Admin Name

   We will keep you updated on the progress.

   Best regards,
   UoG Complaint Management Team
   ```

5. **Test all 6 status changes:**
   - NEW → ASSIGNED (Email #1)
   - ASSIGNED → IN_PROGRESS (Email #2)
   - IN_PROGRESS → RESOLVED (Email #3 - requires resolution notes)
   - Or: IN_PROGRESS → REJECTED (Email #4 - requires rejection reason)
   - RESOLVED → CLOSED (Email #5)

---

### Option 2: Real Gmail Emails (Production Testing)

#### Step 1: Get Gmail App Password

1. **Go to your Gmail account**
2. **Enable 2-Step Verification:**
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification" → Turn it ON

3. **Create App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

#### Step 2: Configure Backend

Edit `backend/.env`:

```env
# Comment out console backend
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Uncomment and configure real email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-actual-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=UoG Complaints <your-actual-email@gmail.com>
```

**Replace:**
- `your-actual-email@gmail.com` → Your real Gmail address
- `abcd efgh ijkl mnop` → The 16-character app password (remove spaces)

#### Step 3: Restart Backend

```bash
# Stop the backend (Ctrl+C)
# Start it again
cd backend
python manage.py runserver
```

#### Step 4: Test with Real Email

1. **Register a new student account with YOUR real email:**
   - Go to: http://localhost:5173/register
   - Use your real email address
   - Complete registration

2. **Create a complaint as that student**

3. **Login as admin and change the status:**
   - Click on the complaint
   - Click "Update Status"
   - Select "Assigned"
   - Click "Update & Send Email"

4. **Check your email inbox:**
   - You should receive a real email within seconds!
   - Check spam folder if you don't see it

---

## 🎬 Complete Testing Workflow

### Scenario: Test All 6 Email Types

#### Setup:
```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

#### Test Flow:

**1. Create Test Accounts (if not already done):**
```bash
cd backend
python manage.py seed_data
```

This creates:
- Student: student@uog.edu.et / password123
- Admin: admin@uog.edu.et / password123

**2. Submit Complaint (as Student):**
- Login: http://localhost:5173/login
- Email: student@uog.edu.et
- Password: password123
- Click "New Complaint"
- Fill form and submit
- **Note the Tracking ID**

**3. Test Status Changes (as Admin):**

Login as admin:
- Email: admin@uog.edu.et
- Password: password123

Go to Dashboard → Click on the complaint

**Change 1: NEW → ASSIGNED**
- Click "Update Status"
- Select "Assigned"
- Click "Update & Send Email"
- ✅ Check console/email for "Assigned" notification

**Change 2: ASSIGNED → IN_PROGRESS**
- Click "Update Status"
- Select "In Progress"
- Click "Update & Send Email"
- ✅ Check console/email for "In Progress" notification

**Change 3: IN_PROGRESS → RESOLVED**
- Click "Update Status"
- Select "Resolved"
- Enter resolution notes: "Issue has been fixed. Tested and working."
- Click "Update & Send Email"
- ✅ Check console/email for "Resolved" notification with notes

**Change 4: Test Rejection (create another complaint)**
- Create new complaint as student
- As admin, change to "Rejected"
- Enter rejection reason: "Duplicate complaint. Please refer to CMP-XXX"
- ✅ Check console/email for "Rejected" notification

**Change 5: RESOLVED → CLOSED**
- Go back to resolved complaint
- Click "Update Status"
- Select "Closed"
- Click "Update & Send Email"
- ✅ Check console/email for "Closed" notification

---

## 📋 Checklist: What You Should See

### In Console Mode:
- [ ] Backend terminal shows email content
- [ ] Email has correct subject line
- [ ] Email has student's name
- [ ] Email has tracking ID
- [ ] Email has status information
- [ ] Email has resolution notes (if resolved)
- [ ] Email has rejection reason (if rejected)

### In Real Email Mode:
- [ ] Email arrives in inbox within seconds
- [ ] Email is from "UoG Complaints <your-email@gmail.com>"
- [ ] Email is properly formatted
- [ ] All details are correct
- [ ] Links work (if any)

---

## 🐛 Troubleshooting

### "I don't see the Update Status button"

**Check:**
1. Are you logged in as admin?
   ```javascript
   // Open browser console (F12)
   console.log(JSON.parse(localStorage.getItem('user')))
   // Should show role: 'admin' or 'super_admin'
   ```

2. Are you on the complaint detail page?
   - URL should be: `http://localhost:5173/complaints/1` (or another ID)

3. Is the frontend running without errors?
   - Check browser console for errors

### "Email not sending in real mode"

**Check:**
1. Gmail App Password is correct (16 characters, no spaces)
2. 2-Step Verification is enabled on Gmail
3. Backend restarted after changing .env
4. Check backend console for error messages
5. Try sending a test email:
   ```bash
   cd backend
   python manage.py shell
   ```
   ```python
   from django.core.mail import send_mail
   send_mail(
       'Test Subject',
       'Test message',
       'your-email@gmail.com',
       ['recipient@example.com'],
       fail_silently=False,
   )
   ```

### "Email goes to spam"

**Solutions:**
1. Mark as "Not Spam" in Gmail
2. Add sender to contacts
3. In production, use a proper domain email (not Gmail)

---

## 🎯 Quick Test Commands

### Test Email Configuration:
```bash
cd backend
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

print("Email Backend:", settings.EMAIL_BACKEND)
print("Email Host:", settings.EMAIL_HOST)
print("From Email:", settings.DEFAULT_FROM_EMAIL)

# Send test email
send_mail(
    'Test Email',
    'This is a test email from UoG Complaint System',
    settings.DEFAULT_FROM_EMAIL,
    ['your-email@gmail.com'],
    fail_silently=False,
)
print("✅ Test email sent!")
```

---

## 📊 Expected Email Examples

### Email 1: Assigned
```
Subject: Your Complaint Has Been Assigned - CMP-ABC123
From: UoG Complaints <noreply@uog.edu.et>
To: student@uog.edu.et

Dear John Doe,

Your complaint has been assigned to a staff member for resolution.

Complaint Details:
- Tracking ID: CMP-ABC123
- Title: Broken projector in Room 301
- Status: Assigned
- Assigned to: Maintenance Team

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
- Assigned to: Maintenance Team

We are working to resolve your issue as quickly as possible.
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
```

---

## ✅ Summary

1. **The Update Status button EXISTS** - Look in the complaint detail page (top-right)
2. **Console mode is ALREADY WORKING** - Check backend terminal for emails
3. **For real emails** - Configure Gmail app password in `.env`
4. **Test all 6 statuses** - Follow the workflow above

Need help? Check the backend console for error messages!
