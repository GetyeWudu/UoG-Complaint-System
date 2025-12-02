# TEST USER CREDENTIALS - UoG Complaint Management System

## ✅ All 10 Role-Specific Dashboards Created

### Test User Accounts

| # | Role | Email | Password | Dashboard Features |
|---|------|-------|----------|-------------------|
| 1 | **Student** | student@test.com | student123 | My complaints, Submit new, Track status |
| 2 | **Academic Staff** | academic@test.com | academic123 | Course-related complaints, Respond to grievances |
| 3 | **Non-Academic Staff** | nonacademic@test.com | nonacademic123 | Assigned complaints, Update status |
| 4 | **Proctor** | proctor@test.com | proctor123 | Exam incidents, Security issues, Investigations |
| 5 | **Department Head** | depthead@test.com | depthead123 | Dept complaints, Staff workload, Approvals |
| 6 | **Dean** | dean@test.com | dean123 | College complaints, Dept comparison, Approvals |
| 7 | **Maintenance** | maintenance@test.com | maintenance123 | Assigned tasks, Location-based work, Photo upload |
| 8 | **Admin** | admin@test.com | admin123 | System-wide view, Assign complaints, Reports |
| 9 | **Super Admin** | superadmin@test.com | superadmin123 | Full system access, User management, Audit logs |
| 10 | **Campus Director** | director@test.com | director123 | Campus overview, Critical incidents, SLA compliance |

---

## 🚀 QUICK START GUIDE

### Start the System

**Terminal 1: Backend**
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```
Backend runs at: http://127.0.0.1:8000

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```
Frontend runs at: http://localhost:5173

---

## ✅ FIXED ISSUES

### 1. Language Support Added to Complaint Form
- ✅ Language switcher now appears on complaint form
- ✅ All labels and placeholders translate to Amharic
- ✅ Form accepts Amharic text input (UTF-8 encoded)
- ✅ Placeholder text explicitly mentions: "You can write in Amharic"

### 2. Amharic Text Submission Fixed
- ✅ Backend properly handles UTF-8 encoded Amharic characters
- ✅ No more "Failed to submit" errors with Amharic text
- ✅ Amharic text stored and displayed correctly

---

## 🧪 TOP 10 TEST CASES

### Test 1: Language Switching on Complaint Form
1. Login as **student@test.com / student123**
2. Click "+ New Complaint"
3. Click language switcher (EN/አማ) in top-right
4. Verify all form labels change to Amharic
5. Switch back to English

**Expected:** Form labels translate correctly

---

### Test 2: Submit Complaint in Amharic
1. Login as **student@test.com / student123**
2. Click "+ New Complaint"
3. Switch to Amharic (አማ)
4. Fill form:
   - ርዕስ: `የክፍል ችግር`
   - መግለጫ: `የክፍል መቀመጫ ተሰብሯል። እባክዎ ይጠግኑት።`
   - አካባቢ: `ህንፃ ሀ፣ ክፍል 301`
5. Click "ቅሬታ ያስገቡ"

**Expected:** 
- Complaint submits successfully
- Tracking ID shown
- Amharic text displays correctly in dashboard

---

### Test 3: All 10 Dashboards
Test each role sees their specific dashboard:

1. **Student Dashboard** (student@test.com)
   - My Complaints list
   - "+ New Complaint" button
   - Statistics: Total, New, In Progress, Resolved

2. **Academic Staff Dashboard** (academic@test.com)
   - Course-related complaints
   - Assigned to me
   - Response actions

3. **Non-Academic Staff Dashboard** (nonacademic@test.com)
   - My assigned complaints
   - Update status options

4. **Proctor Dashboard** (proctor@test.com)
   - Exam incidents
   - Security issues
   - Investigation tools

5. **Department Head Dashboard** (depthead@test.com)
   - Department complaints
   - Staff workload view
   - Pending approvals

6. **Dean Dashboard** (dean@test.com)
   - College-level statistics
   - Department comparison
   - Escalated complaints

7. **Maintenance Dashboard** (maintenance@test.com)
   - Assigned tasks by location
   - Priority tasks
   - Completion tracking

8. **Admin Dashboard** (admin@test.com)
   - System-wide statistics
   - All complaints
   - Assignment tools

9. **Super Admin Dashboard** (superadmin@test.com)
   - Global statistics
   - User activity logs
   - System health

10. **Campus Director Dashboard** (director@test.com)
    - Campus overview
    - Critical incidents
    - SLA compliance metrics

**Expected:** Each role sees different dashboard with role-specific data

---

### Test 4: Complaint Assignment
1. Login as **admin@test.com / admin123**
2. Open any "New" complaint
3. Click "Assign To" → Select **academic@test.com**
4. Change status to "In Progress"
5. Add comment: "Assigned to academic staff"
6. Save
7. Logout, login as **academic@test.com / academic123**
8. Verify complaint appears in dashboard

**Expected:** Assignment successful, complaint visible to assigned user

---

### Test 5: Approval Workflow
1. Login as **academic@test.com / academic123**
2. Open assigned complaint
3. Add resolution notes
4. Request approval (if button available)
5. Logout, login as **depthead@test.com / depthead123**
6. Go to "Pending Approvals"
7. Approve with notes
8. Verify status updates

**Expected:** Approval workflow completes, status changes

---

### Test 6: SLA Breach Detection
In backend terminal:
```bash
cd backend
.\venv\Scripts\activate
python manage.py check_sla
```

**Expected:** Command shows SLA status for all complaints

---

### Test 7: Auto-Escalation
In backend terminal:
```bash
python manage.py check_sla --escalate --notify
```

**Expected:** 
- Breached complaints escalate
- Escalation level increases
- Notifications sent

---

### Test 8: Excel Export
1. Login as **admin@test.com / admin123**
2. Open browser console (F12)
3. Run:
```javascript
fetch('http://127.0.0.1:8000/api/complaints/reports/export/?format=excel', {
  headers: {'Authorization': 'Token ' + localStorage.getItem('token')}
}).then(r => r.blob()).then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'complaints.xlsx';
  a.click();
})
```

**Expected:** Excel file downloads with all complaint data

---

### Test 9: PDF Export
1. Login as **admin@test.com / admin123**
2. In browser console:
```javascript
fetch('http://127.0.0.1:8000/api/complaints/reports/export/?format=pdf', {
  headers: {'Authorization': 'Token ' + localStorage.getItem('token')}
}).then(r => r.blob()).then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'report.pdf';
  a.click();
})
```

**Expected:** PDF file downloads with formatted report

---

### Test 10: Dashboard Auto-Refresh
1. Login as any user
2. Note current statistics
3. Open Developer Tools (F12) → Network tab
4. Wait 30 seconds
5. Observe API calls in Network tab
6. Create new complaint in another browser
7. Wait 30 seconds
8. Verify statistics update automatically

**Expected:** Dashboard refreshes every 30 seconds without page reload

---

## 📝 VERIFICATION CHECKLIST

After testing, verify:

- [ ] Language switcher works on all pages
- [ ] Amharic text input works on complaint form
- [ ] Amharic complaints submit successfully
- [ ] All 10 dashboards load correctly
- [ ] Each role sees appropriate data
- [ ] Complaint assignment works
- [ ] Status updates work
- [ ] Approval workflow functions
- [ ] SLA checking command runs
- [ ] Auto-escalation works
- [ ] Excel export works
- [ ] PDF export works
- [ ] Dashboard auto-refreshes
- [ ] Role-based permissions enforced

---

## 🐛 TROUBLESHOOTING

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### Backend errors
```bash
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Can't login
- Verify user exists: Run `python manage.py seed_test_users` again
- Check credentials match table above
- Clear browser cache and try again

### Amharic text shows as boxes
- Ensure browser supports UTF-8
- Check system has Amharic fonts installed
- Try different browser (Chrome/Firefox recommended)

---

## 🎯 SYSTEM FEATURES

✅ **10 Role-Specific Dashboards**  
✅ **Bilingual Support** (English + Amharic)  
✅ **Amharic Text Input & Display**  
✅ **SLA Tracking & Auto-Escalation**  
✅ **Approval Workflow System**  
✅ **Excel & PDF Export**  
✅ **Real-time Dashboard Updates**  
✅ **AI-Enhanced Priority Assignment**  
✅ **File Attachments Support**  
✅ **Comprehensive Audit Logging**  

---

**System is ready for testing! 🚀**
