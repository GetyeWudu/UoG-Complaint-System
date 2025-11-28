# UoG Complaint Management System - Acceptance Checklist

**Project:** University of Gondar Complaint Management & Feedback System  
**Evaluation Date:** TBD  
**Evaluator:** ___________________

---

## Phase 0: Repository Audit ✅

- [x] Repository cloned and analyzed
- [x] audit.md created with comprehensive analysis
- [x] ROADMAP.md created with detailed milestones
- [x] feature/complete-final-project branch created
- [x] Initial commit pushed

---

## Phase 1: Backend Core & Database

### 1.1 Dependencies & Configuration
- [ ] requirements.txt updated with all dependencies
- [ ] .env.example file created
- [ ] MEDIA_URL and MEDIA_ROOT configured
- [ ] CORS properly configured (not allow all)
- [ ] Email backend configured
- [ ] Rate limiting middleware added
- [ ] Argon2 password hasher configured

### 1.2 Database Schema
- [ ] UserProfile consolidated into CustomUser
- [ ] Super Admin role added
- [ ] Non-academic Staff role added
- [ ] OAuth fields added to CustomUser
- [ ] 2FA fields added to CustomUser
- [ ] ComplaintEvent model created
- [ ] ComplaintComment model created
- [ ] ComplaintFile model created
- [ ] RoutingRule model created
- [ ] EmailTemplate model created
- [ ] ActivityLog model created
- [ ] Category and SubCategory models created
- [ ] PasswordResetToken model created
- [ ] Complaint model updated (priority, sub_category, closed_at, updated_at)
- [ ] All migrations created and applied
- [ ] Seed data script created

### 1.3 Authentication
- [ ] User registration endpoint works
- [ ] Password strength validation implemented
- [ ] Password reset request endpoint works
- [ ] Password reset confirm endpoint works
- [ ] OAuth2 integration scaffold created
- [ ] OAuth callback endpoint works
- [ ] Account linking works (local + OAuth)
- [ ] 2FA setup endpoint works
- [ ] 2FA QR code generation works
- [ ] 2FA verification in login works
- [ ] Backup codes generated and work
- [ ] Rate limiting on auth endpoints works
- [ ] Activity logging for auth events works

### 1.4 File Upload System
- [ ] File type validation works (jpg, jpeg, png, gif, pdf only)
- [ ] File size validation works (max 10MB)
- [ ] Multiple files can be uploaded per complaint
- [ ] ComplaintFile CRUD endpoints work
- [ ] Authenticated file serving works
- [ ] Unauthorized users cannot access files
- [ ] File metadata tracked correctly

### 1.5 Complaint Workflow
- [ ] Auto-routing based on category/campus works
- [ ] Assignment endpoint works
- [ ] Status transition validation works
- [ ] Department Head approval workflow works
- [ ] Comment/messaging endpoints work
- [ ] Notification triggers fire correctly
- [ ] Audit trail records all actions
- [ ] Permission checks prevent unauthorized actions

### 1.6 Email Notifications
- [ ] HTML email templates created
- [ ] Submission confirmation email works
- [ ] Assignment notification email works
- [ ] Status change notification email works
- [ ] Resolution notification email works
- [ ] Password reset email works
- [ ] Emails tested with local SMTP

### 1.7 Testing
- [ ] Unit tests for models pass
- [ ] Unit tests for serializers pass
- [ ] Integration tests for auth endpoints pass
- [ ] Integration tests for complaint endpoints pass
- [ ] Integration tests for file upload pass
- [ ] Test coverage > 70%

---

## Phase 2: Frontend Dashboard & UI

### 2.1 Routing & Navigation
- [ ] React Router implemented
- [ ] All routes work correctly
- [ ] Protected routes redirect to login
- [ ] Navigation components work
- [ ] Breadcrumbs display correctly

### 2.2 Authentication UI
- [ ] Registration form works
- [ ] Password reset flow works
- [ ] OAuth login button works
- [ ] 2FA setup page works
- [ ] 2FA QR code displays
- [ ] 2FA verification works
- [ ] Account linking UI works
- [ ] Form validation works

### 2.3 Role-Based Dashboards
- [ ] Student dashboard works
- [ ] Academic Staff dashboard works
- [ ] Non-academic Staff dashboard works
- [ ] Maintenance Worker dashboard works
- [ ] Department Head dashboard works
- [ ] System Admin dashboard works
- [ ] Super Admin dashboard works
- [ ] Role-specific widgets display correctly

### 2.4 Complaint Management UI
- [ ] Complaint submission form works
- [ ] Multi-file upload works
- [ ] Category selection works
- [ ] Complaint detail view works
- [ ] Timeline displays correctly
- [ ] Threaded comments work
- [ ] File attachments display and download
- [ ] Status change modals work
- [ ] Assignment interface works
- [ ] Approval workflow UI works
- [ ] Anonymous submission works
- [ ] Tracking token displayed correctly

### 2.5 Analytics & Visualizations
- [ ] Trend chart displays correctly
- [ ] Time-to-resolution chart works
- [ ] Heatmap visualization works
- [ ] Status pie chart works
- [ ] Category bar chart works
- [ ] CSV export works
- [ ] Date range filters work
- [ ] Category/department filters work

### 2.6 Advanced Features
- [ ] Language switcher works
- [ ] English translations complete
- [ ] Amharic translations present (at least main UI)
- [ ] Dark mode toggle works
- [ ] Dark mode persists across sessions
- [ ] PWA manifest configured
- [ ] Service worker registered
- [ ] Offline draft storage works
- [ ] Offline sync on reconnect works
- [ ] Toast notifications work
- [ ] Loading states display
- [ ] Error boundaries catch errors

### 2.7 Testing
- [ ] UI unit tests pass
- [ ] E2E tests for core flows pass
- [ ] Cross-browser testing done
- [ ] Mobile responsiveness verified

---

## Phase 3: Analytics & Reporting

### 3.1 Analytics Endpoints
- [ ] GET /api/v1/analytics/trends works
- [ ] GET /api/v1/analytics/time-to-resolution works
- [ ] GET /api/v1/analytics/heatmap works
- [ ] GET /api/v1/analytics/summary works
- [ ] Date range filtering works
- [ ] Category filtering works
- [ ] Department filtering works
- [ ] CSV export parameter works
- [ ] Analytics queries perform well

### 3.2 Reporting System
- [ ] PDF generation for complaints works
- [ ] PDF report generation works
- [ ] CSV export works
- [ ] Admin report UI works
- [ ] Report templates created

### 3.3 Advanced Analytics
- [ ] Response time by department works
- [ ] Staff performance metrics work
- [ ] Category trend analysis works
- [ ] Peak time analysis works
- [ ] Resolution rate tracking works
- [ ] User satisfaction metrics work

### 3.4 Testing
- [ ] Integration tests for analytics pass
- [ ] Export functionality tested

---

## Phase 4: Testing, Documentation & Polish

### 4.1 Testing
- [ ] All backend unit tests pass
- [ ] All backend integration tests pass
- [ ] All frontend unit tests pass
- [ ] All E2E tests pass
- [ ] Test coverage report generated
- [ ] Test coverage > 70%
- [ ] Test data generation script works
- [ ] Test execution documented

### 4.2 API Documentation
- [ ] drf-spectacular or drf-yasg installed
- [ ] API schema generated
- [ ] All endpoints documented
- [ ] Request/response examples added
- [ ] Swagger UI accessible at /api/docs/
- [ ] All endpoints tested in Swagger

### 4.3 Diagrams
- [ ] ER diagram created
- [ ] Use case diagram created
- [ ] Sequence diagram created
- [ ] System architecture diagram created
- [ ] All diagrams in /docs folder

### 4.4 Documentation
- [ ] README.md comprehensive
- [ ] Local setup steps documented
- [ ] Environment variables documented
- [ ] Migration commands documented
- [ ] Troubleshooting section added
- [ ] USER_MANUAL.pdf created
- [ ] PROJECT_REPORT.pdf created
- [ ] demo.md created
- [ ] FINAL_SUBMISSION.md created

### 4.5 Final Polish
- [ ] No console.logs in code
- [ ] No debug prints in code
- [ ] Backend linting passes
- [ ] Frontend linting passes
- [ ] Security audit completed
- [ ] Performance tested
- [ ] Cross-browser tested
- [ ] Mobile responsiveness verified
- [ ] Accessibility audit done (basic WCAG)
- [ ] Backup script created
- [ ] Final testing with seed data done

---

## Functional Requirements

### Authentication & Authorization
- [ ] ✅ Local username/password login works
- [ ] ✅ User registration works
- [ ] ✅ Password reset works
- [ ] ✅ OAuth integration works (with placeholders)
- [ ] ✅ Account linking works
- [ ] ✅ 2FA/TOTP works (optional)
- [ ] ✅ Role-based access control works
- [ ] ✅ All 7 roles implemented

### Complaint Management
- [ ] ✅ Anonymous complaint submission works
- [ ] ✅ Tracking token generated and returned
- [ ] ✅ Non-anonymous complaint works
- [ ] ✅ Email confirmation sent
- [ ] ✅ File uploads work (multiple files)
- [ ] ✅ File validation works (type, size)
- [ ] ✅ Auto-routing works
- [ ] ✅ Manual assignment works
- [ ] ✅ Status updates work
- [ ] ✅ Comments/messaging works
- [ ] ✅ Department Head approval works
- [ ] ✅ Feedback rating works

### Notifications
- [ ] ✅ Submission confirmation email
- [ ] ✅ Assignment notification email
- [ ] ✅ Status change notification email
- [ ] ✅ Resolution notification email
- [ ] ✅ Password reset email

### Analytics
- [ ] ✅ Trends over time
- [ ] ✅ Time-to-resolution metrics
- [ ] ✅ Department/campus heatmap
- [ ] ✅ CSV export
- [ ] ✅ Filtering works

### UI/UX
- [ ] ✅ Modern dashboard design
- [ ] ✅ Responsive design
- [ ] ✅ Role-based dashboards
- [ ] ✅ Multi-language (English + Amharic)
- [ ] ✅ Dark/light mode
- [ ] ✅ PWA with offline support

### Security
- [ ] ✅ Input validation
- [ ] ✅ SQL injection protection
- [ ] ✅ XSS protection
- [ ] ✅ Password hashing (Argon2)
- [ ] ✅ Rate limiting
- [ ] ✅ Activity logging
- [ ] ✅ File upload security
- [ ] ✅ Authenticated file serving

---

## Sample Accounts (Must Exist)

- [ ] student@example.com / Student123! (Student)
- [ ] staff@example.com / Staff123! (Academic Staff)
- [ ] nonstaff@example.com / NonStaff123! (Non-academic Staff)
- [ ] maint@example.com / Maint123! (Maintenance Worker)
- [ ] depthead@example.com / DeptHead123! (Department Head)
- [ ] admin@example.com / Admin123! (System Admin)
- [ ] super@example.com / Super123! (Super Admin)

---

## Deliverables

### Code
- [ ] Backend code complete and working
- [ ] Frontend code complete and working
- [ ] Database migrations present
- [ ] Seed data script present
- [ ] No critical bugs

### Documentation
- [ ] README.md
- [ ] .env.example
- [ ] API documentation (Swagger)
- [ ] ER diagram
- [ ] UML diagrams
- [ ] USER_MANUAL.pdf
- [ ] PROJECT_REPORT.pdf
- [ ] demo.md
- [ ] FINAL_SUBMISSION.md

### Testing
- [ ] Test suite present
- [ ] Tests pass
- [ ] Test coverage > 70%
- [ ] Test execution documented

---

## Final Acceptance Test

### Can the evaluator:
1. [ ] Clone the repository
2. [ ] Follow README to set up locally
3. [ ] Run migrations successfully
4. [ ] Load seed data
5. [ ] Start backend server
6. [ ] Start frontend server
7. [ ] Login with each sample account
8. [ ] Submit anonymous complaint and receive tracking token
9. [ ] Submit non-anonymous complaint and receive email
10. [ ] Department Head assign complaint
11. [ ] Staff update status
12. [ ] Department Head approve closure
13. [ ] View analytics with charts
14. [ ] Export data to CSV
15. [ ] Upload files successfully
16. [ ] View OAuth integration instructions
17. [ ] Enable 2FA for an account
18. [ ] Switch language to Amharic
19. [ ] Toggle dark mode
20. [ ] Use app offline (PWA)

---

**Checklist Complete:** _____ / _____ items  
**Pass/Fail:** _____  
**Evaluator Signature:** ___________________  
**Date:** ___________________
