# Email Setup Guide - Real Gmail Configuration

## 🎯 Goal
Send real email notifications to your actual email address when complaint status changes.

---

## 📧 Step 1: Get Gmail App Password

### 1.1 Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow the steps to enable it
4. **You MUST have 2FA enabled to create app passwords**

### 1.2 Create App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Type: **UoG Complaints**
5. Click **Generate**
6. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)
7. **Save it somewhere safe!**

---

## ⚙️ Step 2: Configure Backend

### 2.1 Edit `.env` File
Open `backend/.env` and update the email section:

```env
# Email Configuration (SMTP)
# Comment out console backend
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Uncomment and configure Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=UoG Complaints <your-email@gmail.com>
ADMIN_EMAIL=admin@uog.edu.et
```

### 2.2 Replace with Your Details
- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: The 16-character app password (with or without spaces)
- `DEFAULT_FROM_EMAIL`: Your Gmail address (this is what students see as sender)

### Example:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=john.doe@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=UoG Complaints <john.doe@gmail.com>
ADMIN_EMAIL=admin@uog.edu.et
```

---

## 🔄 Step 3: Restart Backend

```bash
# Stop the backend (Ctrl+C in the terminal)
# Then restart it
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

---

## 🧪 Step 4: Test Email Notifications

### 4.1 Register with Your Real Email
1. Go to http://localhost:5174/register
2. Register a new student account with **your real email**
3. Example:
   - Email: `your-email@gmail.com`
   - Username: `testuser`
   - Password: `test123`
   - Role: Student

### 4.2 Create a Complaint
1. Login with your new account
2. Click "+ New Complaint"
3. Fill in the form:
   - Title: "Test Email Notification"
   - Description: "Testing if emails work"
   - Location: "Room 101"
4. Click "Submit Complaint"
5. Note the tracking ID

### 4.3 Update Status as Admin
1. **Logout** from student account
2. **Login as admin**:
   - Email: `admin@uog.edu.et`
   - Password: `admin123`
3. Find the test complaint in dashboard
4. **Click on the complaint** to open details
5. **Click "Update Status" button** (new button added!)
6. Select status: **"Assigned"**
7. Click **"Update & Send Email"**

### 4.4 Check Your Email
1. Open your Gmail inbox
2. Look for email from "UoG Complaints"
3. Subject: "Your Complaint Has Been Assigned - CMP-XXXXX"
4. **You should receive the email within 1-2 minutes!**

---

## 📬 Testing All 6 Email Types

### Type 1: Assigned
1. Status: New → **Assigned**
2. Email: "Your complaint has been assigned to a staff member"

### Type 2: In Progress
1. Status: Assigned → **In Progress**
2. Email: "Your complaint is being processed"

### Type 3: Resolved
1. Status: In Progress → **Resolved**
2. Add resolution notes: "Issue has been fixed"
3. Email: "Your complaint has been resolved" + notes

### Type 4: Rejected
1. Status: New → **Rejected**
2. Add rejection reason: "Outside scope of system"
3. Email: "Cannot proceed" + reason

### Type 5: Closed
1. Status: Resolved → **Closed**
2. Email: "Your complaint has been closed"

### Type 6: Reviewed (Generic)
1. Any other status change
2. Email: "Your complaint has been reviewed"

---

## 🎯 Quick Test Workflow

```
1. Register student with YOUR email
   ↓
2. Create complaint
   ↓
3. Login as admin
   ↓
4. Open complaint
   ↓
5. Click "Update Status"
   ↓
6. Select "Assigned"
   ↓
7. Click "Update & Send Email"
   ↓
8. Check YOUR Gmail inbox
   ↓
9. ✅ Email received!
```

---

## 🎨 New UI Features

### "Update Status" Button
- **Location**: Complaint detail page, top right
- **Who sees it**: Admins, dept heads, proctors
- **What it does**: Opens modal to change status

### Status Update Modal
- **Select new status** from dropdown
- **Add resolution notes** (if resolved)
- **Add rejection reason** (if rejected)
- **See email notification reminder**
- **Click "Update & Send Email"**

### Status Options:
- 🟣 **Assigned** - Give to staff member
- 🟡 **In Progress** - Work started
- 🟢 **Resolved** - Issue fixed (requires notes)
- 🔴 **Rejected** - Cannot process (requires reason)
- ⚫ **Closed** - Completed

---

## 🐛 Troubleshooting

### Email Not Sending?

**Check 1: App Password**
- Make sure you copied the full 16-character password
- Spaces don't matter (Gmail ignores them)
- Password should look like: `abcd efgh ijkl mnop`

**Check 2: 2FA Enabled**
- App passwords only work with 2FA enabled
- Check: https://myaccount.google.com/security

**Check 3: .env File**
- Make sure EMAIL_BACKEND is set to smtp (not console)
- Check EMAIL_HOST_USER is your Gmail
- Check EMAIL_HOST_PASSWORD is the app password

**Check 4: Backend Restarted**
- Stop backend (Ctrl+C)
- Start again: `python manage.py runserver`
- Changes to .env require restart

**Check 5: Gmail Security**
- Check if Gmail blocked the login attempt
- Go to: https://myaccount.google.com/notifications
- Allow the app if blocked

### Still Not Working?

**Test with Console Backend First:**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
- Restart backend
- Update status
- Check backend console - email should print there
- If it prints, backend code works
- If not, there's a code issue

**Check Backend Logs:**
- Look at backend terminal for errors
- Should see: "Notification sent to email@example.com"
- If you see errors, read the error message

---

## 📧 Email Examples

### Example 1: Assigned Email
```
From: UoG Complaints <your-email@gmail.com>
To: student@gmail.com
Subject: Your Complaint Has Been Assigned - CMP-ABC12345

Dear John Doe,

Your complaint has been assigned to a staff member for resolution.

Complaint Details:
- Tracking ID: CMP-ABC12345
- Title: Test Email Notification
- Assigned to: Maintenance Team
- Status: Assigned

We will keep you updated on the progress.

Best regards,
UoG Complaint Management Team
```

### Example 2: Resolved Email
```
From: UoG Complaints <your-email@gmail.com>
To: student@gmail.com
Subject: Your Complaint Has Been Resolved - CMP-ABC12345

Dear John Doe,

Great news! Your complaint has been resolved.

Complaint Details:
- Tracking ID: CMP-ABC12345
- Title: Test Email Notification
- Status: Resolved
- Resolution Notes: The issue has been fixed and tested. 
  Everything is working properly now.

If you are satisfied with the resolution, no further action is needed.
If you have any concerns, please contact us.

Best regards,
UoG Complaint Management Team
```

---

## ✅ Success Checklist

- [ ] 2FA enabled on Gmail
- [ ] App password created
- [ ] `.env` file updated with Gmail credentials
- [ ] Backend restarted
- [ ] Registered student with real email
- [ ] Created test complaint
- [ ] Logged in as admin
- [ ] Clicked "Update Status" button
- [ ] Selected new status
- [ ] Clicked "Update & Send Email"
- [ ] Received email in Gmail inbox

---

## 🎉 You're Done!

Once you receive your first email, the system is working perfectly!

Now every time you update a complaint status:
1. Student gets email notification
2. Email includes all complaint details
3. Email is professional and clear
4. Student stays informed automatically

---

## 💡 Pro Tips

1. **Use a dedicated Gmail** for the system (not your personal email)
2. **Keep app password secure** - don't share it
3. **Test with your own email first** before using with real students
4. **Check spam folder** if emails don't appear in inbox
5. **Add resolution notes** when resolving - students appreciate details

---

**Need Help?**
- Check troubleshooting section above
- Review backend console for errors
- Test with console backend first
- Make sure .env changes are saved

**Ready to go live?**
- Use a professional email address
- Update DEFAULT_FROM_EMAIL to match your institution
- Test all 6 email types
- Train admins on using "Update Status" button
