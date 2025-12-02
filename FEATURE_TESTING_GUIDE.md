# Feature Testing Guide
**UoG Complaint Management System**  
**Date:** December 1, 2025

## Prerequisites

### 1. Start the Backend Server
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```
Backend should be running at: http://127.0.0.1:8000

### 2. Start the Frontend Server
```bash
cd frontend
npm start
```
Frontend should be running at: http://localhost:3000

### 3. Verify Test Users Exist
```bash
cd backend
.\venv\Scripts\activate
python manage.py seed_test_users
```

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Student | student | student123 |
| Academic Staff | academic | academic123 |
| Non-Academic Staff | nonacademic | nonacademic123 |
| Proctor | proctor | proctor123 |
| Department Head | depthead | depthead123 |
| Dean | dean | dean123 |
| Maintenance Worker | maintenance | maintenance123 |
| Admin | admin | admin123 |
| Super Admin | superadmin | superadmin123 |
| Campus Director | director | director123 |

---

## Testing Checklist

## 1. STUDENT DASHBOARD TESTING

### Login
1. Go to http://localhost:3000/login
2. Enter username: `student`, password: `student123`
3. Click Login

### Features to Test:
- [ ] **Dashboard loads** - Should see "My Complaints" header
- [ ] **Statistics visible** - Total, Open, Resolved, Average Rating cards
- [ ] **Create complaint button** - "+ New Complaint" button visible
- [ ] **View own complaints** - Only student's complaints shown
- [ ] **Click complaint** - Opens complaint detail page

### Create New Complaint:
1. Click "+ New Complaint" button
2. Fill in:
   - Title: "Test complaint from student"
   - Description: "Testing the complaint system"
   - Location: "Library"
   - Category: Select any
3. Click Submit
4. [ ] **Success message** - Should show tracking ID
5. [ ] **Redirects to dashboard** - New complaint appears in list

### View Complaint Details:
1. Click on any complaint in the list
2. [ ] **Can view details** - Title, description, status visible
3. [ ] **Can add comments** - Comment box should be HIDDEN (students can only view)
4. [ ] **Can view comments** - Existing comments visible
5. [ ] **Can upload files** - File upload section visible
6. [ ] **Can rate** - Rating section visible if resolved

### Logout:
- [ ] Click Logout button - Returns to login page

---

## 2. ACADEMIC STAFF DASHBOARD TESTING

### Login
1. Login with username: `academic`, password: `academic123`

### Features to Test:
- [ ] **Dashboard loads** - "Academic Staff Dashboard" header
- [ ] **Assigned complaints visible** - Only complaints assigned to this user
- [ ] **Cannot see all complaints** - Only assigned ones
- [ ] **Click complaint** - Opens detail page

### Handle Complaint:
1. Click on an assigned complaint
2. [ ] **Can add comments** - Comment box visible (staff can comment)
3. Add comment: "Reviewing this issue"
4. [ ] **Can update status** - Status dropdown available
5. [ ] **Can add resolution** - Resolution notes field available
6. [ ] **Can assign to others** - Assignment dropdown visible

---

## 3. NON-ACADEMIC STAFF DASHBOARD TESTING

### Login
1. Login with username: `nonacademic`, password: `nonacademic123`

### Features to Test:
- [ ] **Dashboard loads** - "Non-Academic Staff Dashboard" header
- [ ] **Assigned complaints visible**
- [ ] **Can handle admin issues** - Registration, finance, library complaints
- [ ] **Can update status and comment**

---

## 4. PROCTOR DASHBOARD TESTING

### Login
1. Login with username: `proctor`, password: `proctor123`

### Features to Test:
- [ ] **Dashboard loads** - "Exam Incidents" header
- [ ] **Statistics visible** - Total incidents, Pending, In Progress, Resolved
- [ ] **Exam complaints list** - Security/exam related complaints
- [ ] **Can investigate** - Click complaint to view details
- [ ] **Can document evidence** - Add comments and files

---

## 5. DEPARTMENT HEAD DASHBOARD TESTING

### Login
1. Login with username: `depthead`, password: `depthead123`

### Features to Test:
- [ ] **Dashboard loads** - "Department Complaints" header
- [ ] **Statistics visible** - Total, New, In Progress, Resolved, Pending Approvals
- [ ] **Staff workload section** - Shows staff members and their assigned complaints
- [ ] **Can view all department complaints**
- [ ] **Can assign complaints** - Assignment feature in detail page
- [ ] **Can approve resolutions** - Approval workflow available

---

## 6. DEAN DASHBOARD TESTING ✨ NEW FEATURES

### Login
1. Login with username: `dean`, password: `dean123`

### Features to Test:
- [ ] **Dashboard loads** - "College Complaints" header with college name
- [ ] **Statistics visible** - Total, Unresolved, SLA Breaches, Avg Resolution Time
- [ ] **Department breakdown** - Shows stats for each department in college
- [ ] **Pending approvals section** - Complaints requiring approval
- [ ] **All complaints table** ✨ NEW - Table showing all college complaints
- [ ] **Can click complaints** - Opens detail page
- [ ] **Can approve major decisions**

---

## 7. MAINTENANCE DASHBOARD TESTING

### Login
1. Login with username: `maintenance`, password: `maintenance123`

### Features to Test:
- [ ] **Dashboard loads** - "Assigned Tasks" header
- [ ] **Statistics visible** - Open Tasks, Completed Tasks
- [ ] **Open tasks list** - Shows pending maintenance work
- [ ] **Can update status** - Mark tasks as complete
- [ ] **Can upload photos** - File upload for completion proof

---

## 8. ADMIN DASHBOARD TESTING

### Login
1. Login with username: `admin`, password: `admin123`

### Features to Test:
- [ ] **Dashboard loads** - "System Overview" header
- [ ] **Statistics visible** - Total, New, In Progress, Resolved, SLA Breaches
- [ ] **Campus breakdown** - Stats by campus
- [ ] **All complaints visible** - Can see every complaint in system
- [ ] **Can assign to anyone** - Full assignment control
- [ ] **Can change any status** - Full status control

---

## 9. SUPER ADMIN DASHBOARD TESTING

### Login
1. Login with username: `superadmin`, password: `superadmin123`

### Features to Test:
- [ ] **Dashboard loads** - "System Stats" header
- [ ] **Statistics visible** - Total complaints, Total users, SLA breaches
- [ ] **Users by role** - Breakdown of users by role
- [ ] **Full system access** - Can see everything
- [ ] **Can access Django admin** - Go to http://127.0.0.1:8000/admin/

---

## 10. CAMPUS DIRECTOR DASHBOARD TESTING

### Login
1. Login with username: `director`, password: `director123`

### Features to Test:
- [ ] **Dashboard loads** - "Campus Overview" header with campus name
- [ ] **Statistics visible** - Total, Critical, Unresolved, SLA Breaches, Compliance %
- [ ] **Critical incidents section** - Shows high-priority complaints
- [ ] **Can handle critical incidents**
- [ ] **SLA compliance tracking**

---

## 11. ANONYMOUS COMPLAINT TRACKING ✨ NEW FEATURES

### Test Anonymous Submission:
1. Logout (if logged in)
2. Go to http://localhost:3000/
3. Click "Submit Anonymous Complaint"
4. Fill in complaint details
5. Submit
6. [ ] **Tracking ID shown** - Copy the tracking ID (e.g., CMP-ABC12345)

### Test Tracking:
1. Go to http://localhost:3000/track
2. Enter the tracking ID
3. Click "Track"
4. [ ] **Complaint details shown** - Title, status, location, priority
5. [ ] **Resolution shown** ✨ NEW - If status is resolved, resolution message appears
6. [ ] **Comments shown** ✨ NEW - All comments with author names and timestamps
7. [ ] **Cannot post comments** - No comment form (anonymous users can only view)

---

## 12. BILINGUAL SUPPORT TESTING

### Test Language Switching:
1. Login as any user
2. [ ] **Language switcher visible** - Flag icons in header
3. Click on Amharic flag (🇪🇹)
4. [ ] **Interface changes to Amharic** - Buttons, labels in Amharic
5. Click on English flag (🇬🇧)
6. [ ] **Interface changes to English**
7. [ ] **Language persists** - Refresh page, language stays the same

---

## 13. COMPLAINT DETAIL PAGE TESTING

### Test as Student:
1. Login as student
2. Open any complaint
3. [ ] **Cannot post comments** ✨ FIXED - Comment form hidden for students
4. [ ] **Can view comments** - Existing comments visible
5. [ ] **Can upload files** - File upload available
6. [ ] **Can rate** - Rating section available if resolved

### Test as Staff:
1. Login as academic/admin
2. Open any complaint
3. [ ] **Can post comments** ✨ FIXED - Comment form visible for staff
4. [ ] **Can update status** - Status dropdown available
5. [ ] **Can assign** - Assignment dropdown available
6. [ ] **Can add resolution** - Resolution notes field available

---

## 14. AI FEATURES TESTING

### Test AI Analysis:
1. Login as student
2. Create a new complaint with description:
   ```
   URGENT: The main water pipe burst in Building A. 
   Water is flooding the entire first floor. 
   This is an emergency situation!
   ```
3. Submit complaint
4. [ ] **AI urgency detected** - Should be marked as "high" or "critical"
5. [ ] **AI summary generated** - Check complaint detail for summary
6. [ ] **Sentiment analyzed** - Sentiment score calculated

---

## 15. SLA TRACKING TESTING

### Test SLA Monitoring:
1. Login as admin or dept head
2. View dashboard statistics
3. [ ] **SLA breaches shown** - Count of SLA violations
4. [ ] **Response time tracked** - Average response time displayed
5. [ ] **Resolution time tracked** - Average resolution time shown

---

## 16. APPROVAL WORKFLOW TESTING

### Test Approval Process:
1. Login as dept head
2. Create/view a complaint that requires approval
3. [ ] **Pending approvals section** - Shows complaints needing approval
4. Open complaint requiring approval
5. [ ] **Approve/Reject buttons** - Approval controls visible
6. Approve the complaint
7. [ ] **Status updated** - Complaint moves forward in workflow

---

## 17. FILE UPLOAD TESTING

### Test File Attachments:
1. Login as student
2. Open a complaint
3. Scroll to "Attachments" section
4. Click "Choose File"
5. Select an image or PDF
6. Click "Upload"
7. [ ] **File uploaded** - File appears in attachments list
8. [ ] **Can download** - Click file to download
9. [ ] **Can delete** - Delete button available (if owner)

---

## 18. NOTIFICATION TESTING

### Test Email Notifications (if configured):
1. Create a new complaint
2. [ ] **Submitter notified** - Email sent to submitter
3. Assign complaint to staff
4. [ ] **Assignee notified** - Email sent to assigned staff
5. Update status to resolved
6. [ ] **Submitter notified** - Email sent about resolution

---

## 19. SEARCH AND FILTER TESTING

### Test Complaint Filtering:
1. Login as admin
2. Go to complaints list
3. [ ] **Can filter by status** - Filter dropdown available
4. [ ] **Can filter by priority** - Priority filter available
5. [ ] **Can search** - Search box available
6. [ ] **Results update** - Filters work correctly

---

## 20. RESPONSIVE DESIGN TESTING

### Test Mobile View:
1. Open browser developer tools (F12)
2. Toggle device toolbar (mobile view)
3. [ ] **Dashboard responsive** - Layout adapts to mobile
4. [ ] **Navigation works** - Menu accessible on mobile
5. [ ] **Forms usable** - Can submit complaints on mobile
6. [ ] **Tables scroll** - Tables scroll horizontally if needed

---

## Common Issues and Solutions

### Backend Not Running
**Symptom:** "Network Error" or "Cannot connect"  
**Solution:**
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

### Frontend Not Running
**Symptom:** Page not loading at localhost:3000  
**Solution:**
```bash
cd frontend
npm start
```

### No Complaints Visible
**Symptom:** Empty dashboard  
**Solution:** Create test complaints as student user first

### Tracking ID Not Working
**Symptom:** "Complaint not found"  
**Solution:** 
1. Ensure backend is running
2. Use correct tracking ID format (CMP-XXXXXXXX)
3. Check if complaint exists in database

### Language Not Switching
**Symptom:** Interface stays in English  
**Solution:** 
1. Clear browser cache
2. Check localStorage in browser dev tools
3. Verify i18n files exist

---

## Quick Test Script

For rapid testing, run these commands:

```bash
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python manage.py runserver

# Terminal 2 - Frontend  
cd frontend
npm start

# Terminal 3 - Create test data
cd backend
.\venv\Scripts\activate
python manage.py seed_test_users
```

Then visit http://localhost:3000 and test each role systematically.

---

## Test Results Template

Use this to track your testing:

```
Date: ___________
Tester: ___________

✅ = Pass | ❌ = Fail | ⚠️ = Partial

[ ] Student Dashboard
[ ] Academic Staff Dashboard  
[ ] Non-Academic Staff Dashboard
[ ] Proctor Dashboard
[ ] Department Head Dashboard
[ ] Dean Dashboard
[ ] Maintenance Dashboard
[ ] Admin Dashboard
[ ] Super Admin Dashboard
[ ] Campus Director Dashboard
[ ] Anonymous Tracking
[ ] Bilingual Support
[ ] AI Features
[ ] SLA Tracking
[ ] File Upload
[ ] Comments System

Notes:
_________________________________
_________________________________
_________________________________
```

---

## Support

If you encounter issues:
1. Check browser console (F12) for errors
2. Check backend terminal for error messages
3. Verify all services are running
4. Check test credentials are correct
5. Ensure database has test data
