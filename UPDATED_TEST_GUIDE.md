# ✅ UPDATED TEST GUIDE - UoG Complaint Management System

## 🔐 CORRECT TEST CREDENTIALS

### All 10 Role-Specific Test Accounts

| # | Role | Email | Password | Dashboard |
|---|------|-------|----------|-----------|
| 1 | **Student** | student@test.com | student123 | Student Dashboard |
| 2 | **Academic Staff** | academic@test.com | academic123 | Academic Staff Dashboard |
| 3 | **Non-Academic Staff** | nonacademic@test.com | nonacademic123 | Non-Academic Staff Dashboard |
| 4 | **Proctor** | proctor@test.com | proctor123 | Proctor Dashboard |
| 5 | **Department Head** | depthead@test.com | depthead123 | Department Head Dashboard |
| 6 | **Dean** | dean@test.com | dean123 | Dean Dashboard |
| 7 | **Maintenance** | maintenance@test.com | maintenance123 | Maintenance Dashboard |
| 8 | **Admin** | admin@test.com | admin123 | Admin Dashboard |
| 9 | **Super Admin** | superadmin@test.com | superadmin123 | Super Admin Dashboard |
| 10 | **Campus Director** | director@test.com | director123 | Campus Director Dashboard |

---

## 🎨 NEW FEATURES ADDED

### 1. ✅ Improved Login Page Design
- **UoG Brand Colors**: Green and gold gradient background (matching official UoG website)
- **Larger Logo**: 128x128px logo with circular gradient background
- **Better Layout**: Cleaner, more professional design
- **Language Switcher**: Added to login page (top-right corner)
- **Test Credentials**: Displayed at bottom for easy access

### 2. ✅ Language Persistence Fixed
- **Automatic Save**: Language preference saves to localStorage
- **Persists Across Pages**: Once you change language, it stays changed
- **Persists Across Sessions**: Language preference survives browser refresh
- **Available Everywhere**: Language switcher on every page for convenience

### 3. ✅ Bilingual Login Page
- All login text translates (English ↔ Amharic)
- Form labels, buttons, links all support both languages
- Test credentials section translates

---

## 🚀 QUICK START

### Terminal 1: Backend
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```
**Backend:** http://127.0.0.1:8000

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
**Frontend:** http://localhost:5173

---

## 🧪 TESTING THE NEW FEATURES

### Test 1: New Login Page Design
1. Open http://localhost:5173
2. Verify:
   - ✅ Green and gold gradient background
   - ✅ Large circular logo (or "UoG" text if image missing)
   - ✅ Clean, professional layout
   - ✅ Language switcher in top-right corner
   - ✅ Test credentials shown at bottom

### Test 2: Language Persistence
1. On login page, click **አማ** (Amharic)
2. Verify all text changes to Amharic
3. Login with: **student@test.com / student123**
4. Verify dashboard is still in Amharic
5. Navigate to "New Complaint" page
6. Verify still in Amharic
7. Refresh browser (F5)
8. Verify language is still Amharic

**Expected:** Language stays Amharic across all pages and after refresh

### Test 3: Login with All 10 Roles
Test each account to verify they work:

**Student:**
```
Email: student@test.com
Password: student123
```
Expected: Student Dashboard with "My Complaints"

**Academic Staff:**
```
Email: academic@test.com
Password: academic123
```
Expected: Academic Staff Dashboard

**Admin:**
```
Email: admin@test.com
Password: admin123
```
Expected: Admin Dashboard with system-wide stats

**Dean:**
```
Email: dean@test.com
Password: dean123
```
Expected: Dean Dashboard with college-level data

**Department Head:**
```
Email: depthead@test.com
Password: depthead123
```
Expected: Department Head Dashboard

**Maintenance:**
```
Email: maintenance@test.com
Password: maintenance123
```
Expected: Maintenance Dashboard with assigned tasks

**Proctor:**
```
Email: proctor@test.com
Password: proctor123
```
Expected: Proctor Dashboard with exam incidents

**Non-Academic Staff:**
```
Email: nonacademic@test.com
Password: nonacademic123
```
Expected: Non-Academic Staff Dashboard

**Super Admin:**
```
Email: superadmin@test.com
Password: superadmin123
```
Expected: Super Admin Dashboard with full system access

**Campus Director:**
```
Email: director@test.com
Password: director123
```
Expected: Campus Director Dashboard

### Test 4: Amharic Complaint Submission
1. Login as **student@test.com / student123**
2. Click language switcher → **አማ**
3. Click **አዲስ ቅሬታ** (New Complaint)
4. Fill form in Amharic:
   - **ርዕስ:** `የክፍል ችግር`
   - **መግለጫ:** `የክፍል መቀመጫ ተሰብሯል። እባክዎ በተቻለ ፍጥነት ይጠግኑት።`
   - **አካባቢ:** `ህንፃ ሀ፣ ክፍል 301`
5. Click **ቅሬታ ያስገቡ**

**Expected:**
- ✅ Complaint submits successfully
- ✅ Tracking ID shown
- ✅ Amharic text displays correctly
- ✅ Complaint appears in dashboard

### Test 5: Language Switcher on All Pages
1. Login as any user
2. Navigate through different pages:
   - Dashboard
   - New Complaint
   - Complaint Details
3. On each page, verify:
   - ✅ Language switcher is visible
   - ✅ Clicking it changes the language
   - ✅ Language preference persists when navigating

---

## 🎨 LOGIN PAGE DESIGN DETAILS

### Color Scheme (UoG Official Colors)
- **Primary Green:** `#166534` (green-800)
- **Secondary Green:** `#15803d` (green-700)
- **Accent Gold:** `#ca8a04` (yellow-600)
- **Background:** Gradient from green-800 → green-700 → yellow-600

### Logo
- **Size:** 128x128px (increased from 96x96px)
- **Style:** Circular with gradient background
- **Fallback:** "UoG" text if image not found

### Layout
- **Card:** White, rounded corners, shadow
- **Inputs:** Larger padding, green focus ring
- **Button:** Green gradient with hover effect
- **Links:** Green color matching brand

---

## 📋 VERIFICATION CHECKLIST

After testing, verify:

- [ ] Login page has green/gold gradient background
- [ ] Logo is large and visible (128x128px)
- [ ] Language switcher works on login page
- [ ] All 10 test accounts login successfully
- [ ] Each role sees their specific dashboard
- [ ] Language preference persists across pages
- [ ] Language preference persists after refresh
- [ ] Amharic text input works on complaint form
- [ ] Amharic complaints submit successfully
- [ ] Language switcher appears on all pages
- [ ] Switching language updates all text immediately

---

## 🐛 TROUBLESHOOTING

### "Invalid credentials" error
**Solution:** Make sure you're using the correct test accounts:
- student@test.com / student123
- admin@test.com / admin123
- dean@test.com / dean123
- etc.

### Language doesn't persist
**Solution:** 
1. Clear browser cache
2. Check browser console for errors
3. Verify localStorage is enabled in browser

### Login page looks wrong
**Solution:**
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Restart frontend dev server

### Can't see logo
**Solution:** Logo fallback shows "UoG" text - this is normal if logo image file doesn't exist

---

## 🎯 SYSTEM STATUS

✅ **10 Role-Specific Dashboards**  
✅ **Bilingual Support** (English + Amharic)  
✅ **Language Persistence** (localStorage)  
✅ **Improved Login Design** (UoG colors)  
✅ **Amharic Text Input & Display**  
✅ **Test Accounts Created** (All 10 roles)  
✅ **SLA Tracking & Escalation**  
✅ **Approval Workflow**  
✅ **Excel & PDF Export**  
✅ **Real-time Updates**  

---

## 📞 QUICK REFERENCE

**Frontend:** http://localhost:5173  
**Backend:** http://127.0.0.1:8000  
**Admin Panel:** http://127.0.0.1:8000/admin  

**Quick Test Account:**
- Email: student@test.com
- Password: student123

**System is ready for comprehensive testing! 🚀**
