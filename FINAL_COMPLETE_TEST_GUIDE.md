# 🎯 COMPLETE TESTING GUIDE - UoG Complaint Management System

## 📋 ALL REGISTERED USERS (22 Total)

### ✅ VERIFIED TEST ACCOUNTS (Passwords Known)

| # | Email | Password | Role | Dashboard |
|---|-------|----------|------|-----------|
| 1 | student@test.com | student123 | Student | Student Dashboard |
| 2 | academic@test.com | academic123 | Academic Staff | Academic Staff Dashboard |
| 3 | nonacademic@test.com | nonacademic123 | Non-Academic Staff | Non-Academic Staff Dashboard |
| 4 | proctor@test.com | proctor123 | Proctor | Proctor Dashboard |
| 5 | depthead@test.com | depthead123 | Department Head | Department Head Dashboard |
| 6 | dean@test.com | dean123 | Dean | Dean Dashboard |
| 7 | maintenance@test.com | maintenance123 | Maintenance Worker | Maintenance Dashboard |
| 8 | admin@test.com | admin123 | Admin | Admin Dashboard |
| 9 | superadmin@test.com | superadmin123 | Super Admin | Super Admin Dashboard |
| 10 | director@test.com | director123 | Campus Director | Campus Director Dashboard |

### ⚠️ OTHER USERS (Passwords Unknown - Created Previously)

| Username | Email | Role |
|----------|-------|------|
| abebe | abebe@uog.edu.et | Student |
| gech | wudugetye@gmail.com | Student |
| staff@example.com | staff@example.com | Academic Staff |
| nonstaff@example.com | nonstaff@example.com | Non-Academic Staff |
| proctor_1 | proc@uog.edu.et | Proctor |
| head_cs | head@uog.edu.et | Department Head |
| depthead@example.com | depthead@example.com | Department Head |
| dean_info | dean@uog.edu.et | Dean |
| maint@example.com | maint@example.com | Maintenance Worker |
| getye | admin@uog.edu.et | Admin |
| admin@example.com | admin@example.com | Admin |
| super@example.com | super@example.com | Super Admin |

---

## 🤖 AI FEATURES IMPLEMENTED

The system has **7 AI-powered features**:

### 1. **Auto-Priority Assignment** (Urgency Analysis)
- Analyzes complaint text using keywords and sentiment
- Assigns priority: Critical, High, Medium, Low
- Provides confidence score and reasoning

### 2. **Sentiment Analysis**
- Uses VADER sentiment analyzer
- Scores from -1 (very negative) to +1 (very positive)
- Labels: Positive, Neutral, Negative

### 3. **Language Detection**
- Automatically detects Amharic vs English
- Supports Amharic Unicode range detection
- Confidence scoring

### 4. **Auto-Translation**
- Translates Amharic complaints to English
- Uses Google Translate API
- Stores both original and translated text

### 5. **Duplicate Detection**
- Compares new complaints with existing ones
- Uses text similarity algorithms
- Prevents duplicate submissions

### 6. **Auto-Routing Suggestions**
- Suggests which department should handle complaint
- Based on keywords and category
- Provides confidence score

### 7. **Auto-Summary Generation**
- Creates concise summaries for quick triage
- Extracts key information
- Max 150 characters

---

## 🧪 TOP 5 AI FEATURE TEST CASES

### **AI Test 1: Auto-Priority Assignment (Critical)**

**Objective:** Test if AI correctly identifies critical urgency

**Steps:**
1. Login as **student@test.com / student123**
2. Click "+ New Complaint"
3. Fill form:
   - **Title:** `Emergency - Fire in Building`
   - **Description:** `There is a fire in Building A, Room 301. Smoke is coming out. This is an emergency! Students are in danger.`
   - **Location:** `Building A, Room 301`
4. Submit complaint
5. Login as **admin@test.com / admin123**
6. View the complaint details

**Expected AI Results:**
- ✅ Priority: **CRITICAL**
- ✅ Confidence: ~90%
- ✅ Reason: "Keyword: 'fire', Keyword: 'danger', Keyword: 'emergency'"
- ✅ Sentiment: Very negative (< -0.6)
- ✅ Auto-summary: "There is a fire in Building A, Room 301..."

---

### **AI Test 2: Auto-Priority Assignment (High)**

**Objective:** Test high priority detection

**Steps:**
1. Login as **student@test.com / student123**
2. Create complaint:
   - **Title:** `Broken Door Lock - Security Issue`
   - **Description:** `The main entrance door lock is broken and not working. This is urgent as it's a security hazard. Anyone can enter the building.`
   - **Location:** `Main Building Entrance`
3. Submit
4. Check as admin

**Expected AI Results:**
- ✅ Priority: **HIGH**
- ✅ Confidence: ~85%
- ✅ Reason: "Keyword: 'broken', Keyword: 'not working', Keyword: 'urgent', Keyword: 'security'"
- ✅ Sentiment: Negative
- ✅ Auto-routing: Suggests Security/Proctor

---

### **AI Test 3: Amharic Language Detection & Translation**

**Objective:** Test AI language detection and auto-translation

**Steps:**
1. Login as **student@test.com / student123**
2. Switch to Amharic (አማ)
3. Create complaint in Amharic:
   - **ርዕስ:** `የክፍል ችግር`
   - **መግለጫ:** `የክፍል መቀመጫ ተሰብሯል። እባክዎ በተቻለ ፍጥነት ይጠግኑት። ተማሪዎች መቀመጫ የላቸውም።`
   - **አካባቢ:** `ህንፃ ሀ፣ ክፍል 301`
4. Submit
5. Login as **admin@test.com / admin123**
6. View complaint details

**Expected AI Results:**
- ✅ Language Detected: **Amharic (am)**
- ✅ Confidence: ~70-85%
- ✅ Original Text: Stored in Amharic
- ✅ Translated Text: Auto-translated to English
- ✅ Translation Provider: "googletrans"
- ✅ Both versions visible to admin

---

### **AI Test 4: Duplicate Detection**

**Objective:** Test if AI detects similar/duplicate complaints

**Steps:**
1. Login as **student@test.com / student123**
2. Create first complaint:
   - **Title:** `WiFi not working in Library`
   - **Description:** `The WiFi connection in the library is not working. Students cannot access the internet for research.`
   - **Location:** `Main Library`
3. Submit and note the tracking ID
4. Create second similar complaint:
   - **Title:** `Internet problem in Library`
   - **Description:** `WiFi is down in the library. Cannot connect to internet. Need urgent fix.`
   - **Location:** `Library Building`
5. Submit
6. Login as **admin@test.com / admin123**
7. Check both complaints

**Expected AI Results:**
- ✅ Duplicate Flag: **is_duplicate = True**
- ✅ Similarity Score: ~70-85%
- ✅ Linked to Original: Shows first complaint ID
- ✅ Admin sees warning: "Similar to complaint #XXX"

---

### **AI Test 5: Sentiment Analysis & Auto-Routing**

**Objective:** Test sentiment scoring and department routing

**Steps:**
1. Login as **student@test.com / student123**
2. Create complaint with strong negative sentiment:
   - **Title:** `Terrible Service at Registration Office`
   - **Description:** `This is absolutely unacceptable! I have been waiting for 3 hours at the registration office and nobody is helping. The staff is rude and unprofessional. This is the worst experience ever. I am extremely frustrated and angry.`
   - **Location:** `Registration Office`
3. Submit
4. Login as **admin@test.com / admin123**
5. View complaint details

**Expected AI Results:**
- ✅ Sentiment Score: **< -0.6** (Very negative)
- ✅ Sentiment Label: **Negative**
- ✅ Confidence: ~80-90%
- ✅ Priority: **HIGH** (due to negative sentiment)
- ✅ Auto-routing: Suggests Administrative department
- ✅ Reason includes: "Very negative sentiment"

---

## 📊 COMPLETE SYSTEM TESTING (20 Test Cases)

### **SECTION A: Authentication & Authorization (3 Tests)**

#### Test A1: Login with All 10 Roles
**Steps:**
1. Test each account from the verified list
2. Verify correct dashboard loads
3. Check role-specific features

**Expected:** Each role sees their specific dashboard

#### Test A2: Language Persistence
**Steps:**
1. Login, switch to Amharic
2. Navigate to different pages
3. Logout and login again

**Expected:** Language stays Amharic throughout

#### Test A3: Role-Based Access Control
**Steps:**
1. Login as Student
2. Try to access admin-only features
3. Verify access denied

**Expected:** Students cannot access admin features

---

### **SECTION B: Complaint Management (5 Tests)**

#### Test B1: Create Complaint (English)
**Steps:**
1. Login as student@test.com
2. Create complaint in English
3. Verify tracking ID generated

**Expected:** Complaint created successfully

#### Test B2: Create Complaint (Amharic)
**Steps:**
1. Login as student@test.com
2. Switch to Amharic
3. Create complaint in Amharic
4. Verify AI translation works

**Expected:** Amharic complaint with English translation

#### Test B3: File Attachment
**Steps:**
1. Create complaint
2. Attach image/PDF file
3. Submit and verify file uploaded

**Expected:** File attached and downloadable

#### Test B4: Complaint Assignment
**Steps:**
1. Login as admin@test.com
2. Assign complaint to staff member
3. Login as staff member
4. Verify complaint appears

**Expected:** Assignment successful

#### Test B5: Status Update
**Steps:**
1. Login as assigned staff
2. Update complaint status
3. Add comment
4. Verify changes saved

**Expected:** Status updated, comment visible

---

### **SECTION C: AI Features (5 Tests)**

Use the 5 AI test cases detailed above:
- AI Test 1: Critical Priority
- AI Test 2: High Priority
- AI Test 3: Amharic Translation
- AI Test 4: Duplicate Detection
- AI Test 5: Sentiment Analysis

---

### **SECTION D: Workflow & Approvals (3 Tests)**

#### Test D1: Approval Request
**Steps:**
1. Login as academic@test.com
2. Open assigned complaint
3. Request approval
4. Login as depthead@test.com
5. Approve request

**Expected:** Approval workflow completes

#### Test D2: Escalation
**Steps:**
1. Create old complaint (or manually set date)
2. Run: `python manage.py check_sla --escalate`
3. Verify complaint escalates

**Expected:** Complaint escalated to higher authority

#### Test D3: Resolution & Closure
**Steps:**
1. Login as staff member
2. Resolve complaint with notes
3. Login as dept head
4. Close complaint

**Expected:** Complaint marked as closed

---

### **SECTION E: Reporting & Analytics (2 Tests)**

#### Test E1: Excel Export
**Steps:**
1. Login as admin@test.com
2. Open browser console
3. Run export command (see below)
4. Verify Excel downloads

**Export Command:**
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

**Expected:** Excel file with all complaints

#### Test E2: PDF Report
**Steps:**
1. Login as admin@test.com
2. Run PDF export command
3. Verify PDF downloads

**PDF Export Command:**
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

**Expected:** PDF report with statistics

---

### **SECTION F: Dashboard Features (2 Tests)**

#### Test F1: Real-time Updates
**Steps:**
1. Login as student
2. Note statistics
3. Wait 30 seconds
4. Verify auto-refresh

**Expected:** Dashboard updates every 30 seconds

#### Test F2: Search & Filter
**Steps:**
1. Login as admin
2. Use search box
3. Apply status filter
4. Apply priority filter

**Expected:** Results filter correctly

---

## 🎯 QUICK TEST CHECKLIST

### Essential Tests (Must Pass)

- [ ] Login with student@test.com / student123
- [ ] Login with admin@test.com / admin123
- [ ] Switch language EN ↔ አማ
- [ ] Create complaint in English
- [ ] Create complaint in Amharic
- [ ] AI assigns priority automatically
- [ ] AI detects language (Amharic)
- [ ] AI translates Amharic to English
- [ ] Assign complaint to staff
- [ ] Update complaint status
- [ ] Dashboard auto-refreshes
- [ ] Excel export works
- [ ] PDF export works
- [ ] SLA check command runs
- [ ] All 10 dashboards load

---

## 🚀 HOW TO START TESTING

### Step 1: Start Servers

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 2: Open Browser
Navigate to: http://localhost:5173

### Step 3: Start Testing
Use the test accounts above and follow test cases

---

## 📊 AI FEATURE VERIFICATION

After running AI tests, verify in database or admin panel:

**Check AI Fields:**
- `urgency` - Auto-assigned priority
- `ai_urgency_confidence` - Confidence score
- `ai_urgency_reason` - Why this priority
- `sentiment_score` - Sentiment value
- `sentiment_label` - Positive/Negative/Neutral
- `language` - Detected language (en/am)
- `description_translated` - Auto-translated text
- `translation_confidence` - Translation confidence
- `is_duplicate` - Duplicate flag
- `duplicate_of` - Link to original complaint
- `ai_summary` - Auto-generated summary

---

## 🎓 TESTING TIPS

1. **Test in Order:** Start with authentication, then basic features, then AI
2. **Use Multiple Browsers:** Test different roles simultaneously
3. **Check Console:** Open browser DevTools (F12) to see errors
4. **Check Backend Logs:** Watch terminal for API errors
5. **Test Edge Cases:** Empty fields, very long text, special characters
6. **Test Amharic:** Use actual Amharic Unicode characters
7. **Test Files:** Upload different file types (JPG, PNG, PDF)
8. **Test Limits:** Try uploading large files (>10MB should fail)

---

## 📈 SUCCESS CRITERIA

### System is working correctly if:

✅ All 10 test accounts can login  
✅ Each role sees their specific dashboard  
✅ Language switching works and persists  
✅ Complaints can be created in English  
✅ Complaints can be created in Amharic  
✅ AI assigns priority automatically  
✅ AI detects Amharic language  
✅ AI translates Amharic to English  
✅ AI detects duplicate complaints  
✅ AI analyzes sentiment correctly  
✅ Complaints can be assigned  
✅ Status can be updated  
✅ Approval workflow works  
✅ SLA checking works  
✅ Excel export works  
✅ PDF export works  
✅ Dashboard auto-refreshes  
✅ Search and filters work  
✅ File attachments work  
✅ All dashboards load without errors  

---

**TOTAL TEST CASES: 20**  
**AI-SPECIFIC TESTS: 5**  
**VERIFIED ACCOUNTS: 10**  

**Happy Testing! 🎉**
