# 🔍 Where is the "Update Status" Button?

## 📍 Visual Guide

```
┌─────────────────────────────────────────────────────────────┐
│  UoG Complaint Management System                    [Logout]│
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ← Back to Dashboard                                         │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                         │  │
│  │  Broken Projector in Room 301          ┌──────────┐   │  │
│  │  Tracking ID: CMP-ABC123               │   NEW    │   │  │
│  │                                         └──────────┘   │  │
│  │                                         ┌──────────────┐ │
│  │                                         │Update Status │ │ ← HERE!
│  │                                         └──────────────┘ │
│  │                                                         │  │
│  │  Description                                            │  │
│  │  The projector in room 301 is not working...           │  │
│  │                                                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Step-by-Step to Find It

### Step 1: Login as Admin
```
URL: http://localhost:5173/login

Credentials:
Email: admin@uog.edu.et
Password: password123
```

### Step 2: Go to Dashboard
```
After login, you'll see the Dashboard with all complaints listed
```

### Step 3: Click on ANY Complaint
```
Click on any complaint card or row
This opens the Complaint Detail page
```

### Step 4: Look at Top-Right Corner
```
You'll see:
┌──────────────────────────┐
│ Status Badge (colored)   │
│ e.g., "NEW" or "ASSIGNED"│
└──────────────────────────┘
         ↓
┌──────────────────────────┐
│   Update Status Button   │ ← This is what you're looking for!
│   (Blue button)          │
└──────────────────────────┘
```

## 🖼️ What It Looks Like

### For Admin Users:
```
┌─────────────────────────────────────────┐
│ Complaint Title                         │
│ Tracking ID: CMP-123                    │
│                                         │
│                          [  ASSIGNED  ] │ ← Status Badge
│                          [Update Status]│ ← Button (Blue)
└─────────────────────────────────────────┘
```

### For Regular Students:
```
┌─────────────────────────────────────────┐
│ Complaint Title                         │
│ Tracking ID: CMP-123                    │
│                                         │
│                          [  ASSIGNED  ] │ ← Status Badge
│                          (no button)    │ ← Students don't see button
└─────────────────────────────────────────┘
```

## 🎬 What Happens When You Click It?

### A Modal Pops Up:
```
┌─────────────────────────────────────────────────┐
│  Update Complaint Status                    [X] │
├─────────────────────────────────────────────────┤
│                                                 │
│  Current Status: NEW                            │
│                                                 │
│  New Status *                                   │
│  ┌───────────────────────────────────────────┐ │
│  │ Select Status                          ▼  │ │
│  └───────────────────────────────────────────┘ │
│    Options:                                     │
│    - Assigned                                   │
│    - In Progress                                │
│    - Resolved                                   │
│    - Rejected                                   │
│    - Closed                                     │
│                                                 │
│  📧 Email Notification: The student will        │
│     automatically receive an email when you     │
│     update the status.                          │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │Update & Send Email│  │     Cancel      │   │
│  └──────────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────┘
```

## 🔐 Who Can See This Button?

### ✅ Can See Button:
- Admin (role: `admin`)
- Super Admin (role: `super_admin`)
- Department Head (role: `dept_head`)
- Proctor (role: `proctor`)

### ❌ Cannot See Button:
- Student (role: `student`)
- Guest (not logged in)

## 🧪 Quick Test

### Check Your Role:
1. Open browser console (Press F12)
2. Type:
   ```javascript
   JSON.parse(localStorage.getItem('user'))
   ```
3. Look at the `role` field
4. If it says `"student"`, you won't see the button
5. If it says `"admin"`, you WILL see the button

### Switch to Admin:
```bash
# Logout from current account
# Login with admin credentials:
Email: admin@uog.edu.et
Password: password123
```

## 📱 Mobile View

On mobile devices, the button appears below the status badge:

```
┌─────────────────────────┐
│ Complaint Title         │
│ Tracking ID: CMP-123    │
│                         │
│      [  ASSIGNED  ]     │
│                         │
│    [Update Status]      │ ← Button stacks below
└─────────────────────────┘
```

## 🎯 Still Can't Find It?

### Checklist:
- [ ] Backend is running (`python manage.py runserver`)
- [ ] Frontend is running (`npm run dev`)
- [ ] Logged in as admin (not student)
- [ ] On complaint detail page (URL: `/complaints/1`)
- [ ] No JavaScript errors in console (F12)
- [ ] Page fully loaded

### Debug Steps:
1. **Check if you're on the right page:**
   - URL should be: `http://localhost:5173/complaints/[number]`
   - NOT: `http://localhost:5173/dashboard`

2. **Check your role:**
   ```javascript
   // In browser console (F12)
   const user = JSON.parse(localStorage.getItem('user'));
   console.log('Role:', user.role);
   console.log('Is Admin:', ['admin', 'super_admin', 'dept_head', 'proctor'].includes(user.role));
   ```

3. **Check if button is hidden by CSS:**
   ```javascript
   // In browser console
   document.querySelector('button:contains("Update Status")')
   ```

4. **Refresh the page:**
   - Press Ctrl+F5 (hard refresh)
   - Clear browser cache

## 🎬 Video-Style Walkthrough

```
Scene 1: Login
→ Go to http://localhost:5173/login
→ Enter: admin@uog.edu.et / password123
→ Click "Login"

Scene 2: Dashboard
→ You see list of complaints
→ Each complaint shows: Title, Status, Date

Scene 3: Open Complaint
→ Click on any complaint
→ Page changes to complaint detail

Scene 4: Find Button
→ Scroll to top of page
→ Look at right side
→ See status badge (colored pill)
→ See "Update Status" button below it

Scene 5: Click Button
→ Click "Update Status"
→ Modal appears
→ Select new status
→ Click "Update & Send Email"
→ Success! Email sent!
```

## 📞 Need More Help?

If you still can't find the button:

1. **Take a screenshot** of your complaint detail page
2. **Check browser console** (F12) for errors
3. **Verify your role** using the console command above
4. **Make sure you're logged in as admin**

The button is definitely there - it's in the code at line 146-152 of `ComplaintDetail.jsx`!
