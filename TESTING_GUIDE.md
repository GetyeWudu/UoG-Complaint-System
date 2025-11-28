# Testing Guide - UoG Complaint Management System

## Quick Test Checklist

### ✅ Test 1: Comment System
1. Login as student (student@uog.edu.et / student123)
2. Click on any complaint in dashboard
3. Scroll to "Comments" section at bottom
4. Type a comment in the textarea
5. Click "Post Comment"
6. **Expected**: Comment appears immediately with your name and timestamp
7. Refresh page - comment should still be there

### ✅ Test 2: Notification System
1. Login as student
2. Create a new complaint
3. Note the tracking ID
4. Logout
5. Login as admin (admin@uog.edu.et / admin123)
6. Find the complaint in dashboard
7. Click on it to open details
8. Change status from "new" to "assigned"
9. **Expected**: 
   - Backend console shows email being sent (if using console backend)
   - Status updates successfully
10. Logout and login as student
11. **Expected**:
    - Bell icon shows notification badge
    - Click bell to see "Status changed" notification
    - Complaint card shows "ASSIGNED" status

### ✅ Test 3: Search and Filters
1. Login as any user with multiple complaints
2. In dashboard, type in search box
3. **Expected**: Results filter as you type
4. Clear search
5. Select a status filter (e.g., "New")
6. **Expected**: Only complaints with that status show
7. Select a priority filter (e.g., "High")
8. **Expected**: Results further filtered
9. Click "Clear filters"
10. **Expected**: All complaints show again

### ✅ Test 4: Activity Timeline
1. Login and open any complaint
2. Scroll to "Activity Timeline" section
3. **Expected**: See all events (created, status changes, etc.)
4. Each event shows:
   - Description of what happened
   - Timestamp
   - Username of who did it

### ✅ Test 5: Create Complaint (Pagination Fix)
1. Login as student
2. Click "+ New Complaint"
3. **Expected**: Form loads with campus dropdown populated
4. Console shows: "Campuses loaded: 3 campuses" (or however many you have)
5. Fill form and submit
6. **Expected**: Success message with tracking ID

## Detailed Testing Scenarios

### Scenario 1: Full Complaint Lifecycle

**As Student:**
1. Login as student@uog.edu.et
2. Click "+ New Complaint"
3. Fill in:
   - Title: "Broken projector in Room 301"
   - Description: "The projector is not turning on"
   - Location: "Room 301, Building A"
   - Campus: Select any
4. Upload a photo (optional)
5. Click "Submit Complaint"
6. **Verify**: Success alert with tracking ID
7. **Verify**: Redirected to dashboard
8. **Verify**: New complaint appears in list with "NEW" status

**As Admin:**
1. Logout and login as admin@uog.edu.et
2. **Verify**: See the new complaint in dashboard
3. Click on the complaint
4. **Verify**: See all details including description, location, files
5. Change status to "Assigned"
6. **Verify**: Backend console shows email sent
7. Add a comment: "We will send a technician"
8. Click "Post Comment"
9. **Verify**: Comment appears

**Back as Student:**
1. Logout and login as student@uog.edu.et
2. **Verify**: Bell icon has notification badge
3. Click bell icon
4. **Verify**: See "Status changed from new to assigned"
5. Click on the complaint
6. **Verify**: Status shows "ASSIGNED"
7. **Verify**: Activity timeline shows status change
8. **Verify**: See admin's comment
9. Add reply comment: "Thank you!"
10. **Verify**: Comment appears

**Resolve as Admin:**
1. Logout and login as admin
2. Open the complaint
3. Change status to "Resolved"
4. Add resolution notes: "Projector has been replaced"
5. **Verify**: Email sent to student
6. **Verify**: Resolution notes appear in green box

**Final Check as Student:**
1. Login as student
2. **Verify**: Bell shows new notification
3. Open complaint
4. **Verify**: Status is "RESOLVED"
5. **Verify**: Resolution notes visible in green box
6. **Verify**: Activity timeline shows all events

### Scenario 2: Search and Filter

**Setup:**
Create 5 complaints with different statuses and priorities:
1. "AC not working" - New - High
2. "Broken chair" - Assigned - Low
3. "Noisy fan" - In Progress - Medium
4. "Dirty classroom" - Resolved - Low
5. "No internet" - New - Critical

**Test Search:**
1. Type "AC" in search box
2. **Verify**: Only "AC not working" shows
3. Type "broken"
4. **Verify**: Only "Broken chair" shows
5. Clear search

**Test Status Filter:**
1. Select "New" from status dropdown
2. **Verify**: Only 2 complaints show (AC and internet)
3. Select "Resolved"
4. **Verify**: Only "Dirty classroom" shows

**Test Priority Filter:**
1. Clear status filter (select "All Status")
2. Select "Critical" from priority dropdown
3. **Verify**: Only "No internet" shows
4. Select "Low"
5. **Verify**: 2 complaints show (chair and classroom)

**Test Combined Filters:**
1. Type "no" in search
2. Select "New" status
3. Select "Critical" priority
4. **Verify**: Only "No internet" shows
5. Click "Clear filters"
6. **Verify**: All 5 complaints show

### Scenario 3: Notification Bell

**Test Real-time Updates:**
1. Login as student in one browser
2. Login as admin in another browser (or incognito)
3. As admin, change a student's complaint status
4. Wait 30 seconds (auto-refresh interval)
5. **Verify**: Student's bell icon updates with badge
6. Click bell as student
7. **Verify**: New notification appears

**Test Notification Dropdown:**
1. Click bell icon
2. **Verify**: Dropdown appears with recent activity
3. **Verify**: Each notification shows:
   - Action description
   - Timestamp
4. Click outside dropdown
5. **Verify**: Dropdown closes

### Scenario 4: Comments Thread

**Test Comment Creation:**
1. Open any complaint
2. Scroll to comments section
3. Type: "This is a test comment"
4. Click "Post Comment"
5. **Verify**: Button shows "Posting..." briefly
6. **Verify**: Comment appears with your name
7. **Verify**: Timestamp is current
8. Refresh page
9. **Verify**: Comment persists

**Test Multiple Comments:**
1. Add 3 different comments
2. **Verify**: All appear in order
3. **Verify**: Each has correct author name
4. Login as different user
5. Add a comment
6. **Verify**: Shows different author name

**Test Empty State:**
1. Create a new complaint
2. Open it immediately
3. Scroll to comments
4. **Verify**: Shows "No comments yet"

## Common Issues and Solutions

### Issue: "Campuses loaded: Object" in console
**Status**: ✅ Fixed
**Solution**: This is just the console log format. The actual data is extracted correctly.

### Issue: Comment submission fails with 400 error
**Status**: ✅ Fixed
**Solution**: Updated serializer to make complaint and parent read-only fields.

### Issue: Comments show "undefined" for author name
**Status**: ✅ Fixed
**Solution**: Changed from `user_name` to `author_name` to match API.

### Issue: Activity timeline shows nothing
**Status**: ✅ Fixed
**Solution**: Changed from `description` to `notes` field.

### Issue: Empty screen on create complaint
**Status**: ✅ Fixed
**Solution**: Added pagination handling for campus data.

## Performance Testing

### Load Time Expectations
- Dashboard load: < 2 seconds
- Complaint detail: < 1 second
- Search results: Instant (< 100ms)
- Comment submission: < 500ms
- File upload: Depends on file size

### Auto-refresh Testing
1. Open dashboard
2. Wait 30 seconds
3. **Verify**: Network tab shows new API calls
4. **Verify**: Data refreshes without page reload

## Browser Compatibility

Test in:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## API Endpoint Testing

### Test with curl or Postman:

**Get Campuses:**
```bash
curl http://127.0.0.1:8000/api/auth/campuses/
```
Expected: JSON with `count`, `next`, `previous`, `results`

**Get Complaints:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/complaints/
```

**Create Comment:**
```bash
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Test comment"}' \
  http://127.0.0.1:8000/api/complaints/1/comments/
```

## Email Testing

### Console Backend (Development)
1. Check `backend/.env` has:
   ```
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```
2. Watch backend terminal when status changes
3. **Verify**: Email content prints to console

### SMTP Backend (Production)
1. Configure SMTP settings in `.env`
2. Change complaint status
3. Check recipient's email inbox
4. **Verify**: Email received with correct content

## Troubleshooting Commands

### Backend Issues
```bash
# Check for errors
cd backend
.\venv\Scripts\activate
python manage.py check

# View logs
python manage.py runserver
# Watch console output

# Test database
python manage.py dbshell
```

### Frontend Issues
```bash
# Check for errors
cd frontend
npm run dev
# Watch console output

# Clear cache
rm -rf node_modules
npm install
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
cd backend
del db.sqlite3
python manage.py migrate
python manage.py seed_data
```

## Success Criteria

All tests pass when:
- ✅ Comments can be created and viewed
- ✅ Notifications appear in bell icon
- ✅ Emails are sent (console or real)
- ✅ Search filters results correctly
- ✅ Status filters work
- ✅ Priority filters work
- ✅ Combined filters work together
- ✅ Activity timeline shows events
- ✅ Auto-refresh updates data
- ✅ No console errors
- ✅ No 400/500 API errors
- ✅ UI is responsive
- ✅ Loading states show correctly

## Next Steps After Testing

1. ✅ All tests pass → Ready for production
2. ❌ Some tests fail → Check troubleshooting section
3. 🔧 Need changes → Update code and retest
4. 📝 Found bugs → Document and fix
5. 🚀 Ready to deploy → Follow deployment guide

## Test Report Template

```
Date: ___________
Tester: ___________

Test 1 - Comments: ☐ Pass ☐ Fail
Test 2 - Notifications: ☐ Pass ☐ Fail
Test 3 - Search/Filters: ☐ Pass ☐ Fail
Test 4 - Activity Timeline: ☐ Pass ☐ Fail
Test 5 - Create Complaint: ☐ Pass ☐ Fail

Issues Found:
1. ___________
2. ___________

Notes:
___________
```
