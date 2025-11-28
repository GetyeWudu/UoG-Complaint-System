# UoG Complaint Management System - Development Roadmap

**Project:** University of Gondar Complaint Management & Feedback System  
**Branch:** feature/complete-final-project  
**Start Date:** November 28, 2025  
**Target Completion:** December 16, 2025 (19 days)

---

## Phase 0: Repository Audit & Setup ✅
**Duration:** Day 1 (November 28, 2025)  
**Status:** COMPLETED

### Tasks
- [x] Clone and analyze repository structure
- [x] Document current tech stack and dependencies
- [x] Identify missing dependencies
- [x] Analyze database schema and identify gaps
- [x] Review authentication flow
- [x] Assess security vulnerabilities
- [x] Create audit.md document
- [x] Create feature/complete-final-project branch
- [x] Create ROADMAP.md with milestones

### Deliverables
- ✅ audit.md
- ✅ ROADMAP.md
- ✅ feature/complete-final-project branch

---

## Phase 1: Backend Core & Database
**Duration:** Days 2-8 (November 29 - December 5, 2025)  
**Status:** PENDING

### Milestone 1.1: Dependencies & Configuration (Day 2)
- [ ] Update requirements.txt with all missing dependencies
- [ ] Create .env.example file with all required environment variables
- [ ] Configure MEDIA_URL and MEDIA_ROOT in settings.py
- [ ] Set up proper CORS configuration
- [ ] Configure email backend (SMTP settings)
- [ ] Add security middleware and rate limiting
- [ ] Configure password hashers (Argon2)

### Milestone 1.2: Database Schema Refactoring (Days 3-4)
- [ ] Consolidate UserProfile into CustomUser model
- [ ] Add Super Admin and Non-academic Staff roles
- [ ] Add OAuth fields to CustomUser (oauth_provider, oauth_id, oauth_linked_at)
- [ ] Add 2FA fields (totp_secret, totp_enabled, backup_codes)
- [ ] Create ComplaintEvent model (audit trail)
- [ ] Create ComplaintComment model (threaded messaging)
- [ ] Create ComplaintFile model (multiple attachments)
- [ ] Create RoutingRule model (auto-assignment)
- [ ] Create EmailTemplate model
- [ ] Create ActivityLog model (system-wide audit)
- [ ] Create Category and SubCategory models
- [ ] Create PasswordResetToken model
- [ ] Update Complaint model (add priority, sub_category, closed_at, updated_at)
- [ ] Create and run migrations
- [ ] Create seed data script with sample accounts

### Milestone 1.3: Authentication System (Day 5)
- [ ] Implement user registration endpoint
- [ ] Add password strength validation
- [ ] Implement password reset flow (request + confirm)
- [ ] Create OAuth2 integration scaffold (generic OAuth2)
- [ ] Implement account linking (local + OAuth)
- [ ] Add TOTP 2FA setup endpoint
- [ ] Add TOTP 2FA verification in login
- [ ] Generate QR codes for 2FA setup
- [ ] Implement backup codes for 2FA
- [ ] Add rate limiting to auth endpoints
- [ ] Create activity logging for auth events

### Milestone 1.4: File Upload System (Day 6)
- [ ] Implement server-side file validation (type, size)
- [ ] Create ComplaintFile CRUD endpoints
- [ ] Implement authenticated file serving
- [ ] Support multiple file uploads per complaint
- [ ] Add file metadata tracking
- [ ] Implement file deletion with permission checks
- [ ] Add image thumbnail generation (optional)

### Milestone 1.5: Complaint Workflow & Assignment (Day 7)
- [ ] Implement auto-routing based on category/campus
- [ ] Create assignment endpoints (assign to staff)
- [ ] Implement status transition validation
- [ ] Create approval workflow (Dept Head approval)
- [ ] Add comment/messaging endpoints
- [ ] Implement notification triggers
- [ ] Create audit trail for all actions
- [ ] Add permission checks for all operations

### Milestone 1.6: Email Notifications (Day 8)
- [ ] Create HTML email templates (submission, assignment, status change, resolution)
- [ ] Implement email service layer
- [ ] Add email sending on complaint submission
- [ ] Add email on assignment
- [ ] Add email on status change
- [ ] Add email on resolution
- [ ] Add password reset email
- [ ] Test with local SMTP (Mailtrap or similar)

### Phase 1 Deliverables
- Updated requirements.txt
- .env.example file
- Database migrations
- Seed data script with test accounts
- Authentication endpoints (register, login, password reset, OAuth, 2FA)
- File upload system with validation
- Complaint workflow with assignment
- Email notification system
- Activity logging
- Unit tests for models and services
- Integration tests for API endpoints

---

## Phase 2: Frontend Dashboard & UI
**Duration:** Days 9-13 (December 6-10, 2025)  
**Status:** PENDING

### Milestone 2.1: Routing & Navigation (Day 9)
- [ ] Implement React Router for proper navigation
- [ ] Create route structure (login, register, dashboard, complaint detail, settings)
- [ ] Add protected routes with auth checks
- [ ] Create navigation components (sidebar, header)
- [ ] Implement breadcrumbs

### Milestone 2.2: Authentication UI (Day 9)
- [ ] Create registration form
- [ ] Add password reset flow UI
- [ ] Implement OAuth login button with redirect
- [ ] Create 2FA setup page with QR code
- [ ] Add 2FA verification in login
- [ ] Implement account linking UI
- [ ] Add form validation

### Milestone 2.3: Role-Based Dashboards (Days 10-11)
- [ ] Student dashboard (my complaints, submit new, track by token)
- [ ] Staff dashboard (assigned complaints, queue, quick actions)
- [ ] Department Head dashboard (department complaints, assign, approve)
- [ ] Maintenance Worker dashboard (task list, update status)
- [ ] Admin dashboard (system summary, user management, analytics)
- [ ] Super Admin dashboard (all admin features + system config)
- [ ] Create role-specific widgets and cards

### Milestone 2.4: Complaint Management UI (Day 11)
- [ ] Enhanced complaint submission form (multi-file upload, category selection)
- [ ] Complaint detail view with timeline
- [ ] Threaded comments/chat interface
- [ ] File attachment display and download
- [ ] Status change modals with reason input
- [ ] Assignment interface for Dept Heads
- [ ] Approval workflow UI
- [ ] Anonymous complaint submission with tracking token display

### Milestone 2.5: Analytics & Visualizations (Day 12)
- [ ] Time-series trend chart (complaints over time)
- [ ] Time-to-resolution histogram
- [ ] Department/campus heatmap visualization
- [ ] Status distribution pie chart
- [ ] Category breakdown bar chart
- [ ] Export to CSV functionality
- [ ] Date range filters
- [ ] Category/department filters

### Milestone 2.6: Advanced Features (Day 13)
- [ ] Multi-language support (English + Amharic)
- [ ] Language switcher component
- [ ] Translation files (i18n setup)
- [ ] Dark/light mode toggle
- [ ] PWA configuration (manifest, service worker)
- [ ] Offline draft storage (IndexedDB)
- [ ] Offline sync on reconnect
- [ ] Toast notifications for better UX
- [ ] Loading states and skeletons
- [ ] Error boundaries

### Phase 2 Deliverables
- Complete React Router implementation
- Registration and password reset UI
- OAuth and 2FA UI
- Role-based dashboards for all 7 roles
- Enhanced complaint management interface
- Analytics dashboard with charts
- Multi-language support (English + Amharic)
- Dark mode
- PWA with offline support
- UI unit tests
- E2E tests for core flows

---

## Phase 3: Analytics & Reporting
**Duration:** Days 14-16 (December 11-13, 2025)  
**Status:** PENDING

### Milestone 3.1: Analytics Endpoints (Day 14)
- [ ] GET /api/v1/analytics/trends (complaints over time)
- [ ] GET /api/v1/analytics/time-to-resolution (median, mean, distribution)
- [ ] GET /api/v1/analytics/heatmap (department/campus aggregation)
- [ ] GET /api/v1/analytics/summary (overall stats)
- [ ] Add filtering (date range, category, department, campus)
- [ ] Implement CSV export parameter
- [ ] Add caching for performance
- [ ] Create analytics service layer

### Milestone 3.2: Reporting System (Day 15)
- [ ] PDF generation for individual complaints
- [ ] PDF report generation for filtered data
- [ ] CSV export for analytics data
- [ ] Admin report generation UI
- [ ] Report templates
- [ ] Scheduled reports (optional)

### Milestone 3.3: Advanced Analytics (Day 16)
- [ ] Response time analysis by department
- [ ] Staff performance metrics
- [ ] Category trend analysis
- [ ] Peak time analysis
- [ ] Resolution rate tracking
- [ ] User satisfaction metrics (feedback ratings)

### Phase 3 Deliverables
- Analytics API endpoints with filtering
- CSV export functionality
- PDF generation for complaints and reports
- Advanced analytics dashboard
- Performance metrics
- Integration tests for analytics

---

## Phase 4: Testing, Documentation & Polish
**Duration:** Days 17-19 (December 14-16, 2025)  
**Status:** PENDING

### Milestone 4.1: Testing (Day 17)
- [ ] Backend unit tests (models, serializers, services)
- [ ] Backend integration tests (API endpoints)
- [ ] Frontend unit tests (components)
- [ ] Frontend E2E tests (Playwright or Cypress)
- [ ] Test coverage report
- [ ] Fix failing tests
- [ ] Create test data generation script
- [ ] Document test execution steps

### Milestone 4.2: API Documentation (Day 17)
- [ ] Install drf-spectacular or drf-yasg
- [ ] Add API schema generation
- [ ] Document all endpoints with descriptions
- [ ] Add request/response examples
- [ ] Configure Swagger UI at /api/docs/
- [ ] Test all endpoints in Swagger

### Milestone 4.3: Diagrams & Architecture (Day 18)
- [ ] Create ER diagram (database schema)
- [ ] Create use case diagram (system overview)
- [ ] Create sequence diagram (complaint lifecycle)
- [ ] Create system architecture diagram
- [ ] Export diagrams as PNG/SVG
- [ ] Add diagrams to /docs folder

### Milestone 4.4: Documentation (Day 18)
- [ ] Write comprehensive README.md
- [ ] Document local setup steps
- [ ] Document environment variables
- [ ] Document migration commands
- [ ] Add troubleshooting section
- [ ] Create USER_MANUAL.pdf (Student, Staff, Dept Head, Admin guides)
- [ ] Create PROJECT_REPORT.pdf (methodology, technologies, setup)
- [ ] Create demo.md (10-minute demo script)
- [ ] Create CHECKLIST.md (acceptance criteria)

### Milestone 4.5: Final Polish & QA (Day 19)
- [ ] Code cleanup (remove console.logs, debug prints)
- [ ] Linting (backend and frontend)
- [ ] Security audit
- [ ] Performance testing
- [ ] Cross-browser testing
- [ ] Mobile responsiveness check
- [ ] Accessibility audit (WCAG basics)
- [ ] Create backup script
- [ ] Final testing with seed data
- [ ] Create FINAL_SUBMISSION.md

### Phase 4 Deliverables
- Complete test suite with coverage report
- API documentation (Swagger)
- ER diagram, UML diagrams
- Comprehensive README.md
- User manual (PDF)
- Project report (PDF)
- Demo script
- Acceptance checklist
- Final submission document
- Clean, production-ready code

---

## Acceptance Criteria Checklist

### Core Functionality
- [ ] Anonymous complaint submission with tracking token
- [ ] Non-anonymous complaint with email confirmation
- [ ] Local username/password authentication
- [ ] University OAuth integration (with placeholders)
- [ ] Account linking (local + OAuth)
- [ ] Optional 2FA/TOTP
- [ ] File uploads with validation (max 10MB, jpg/png/gif/pdf)
- [ ] Multiple file attachments per complaint
- [ ] Auto-routing based on category/campus
- [ ] Department Head assignment workflow
- [ ] Staff can update status and add comments
- [ ] Department Head approval for closure
- [ ] Email notifications (submission, assignment, status change, resolution)
- [ ] Threaded comments/messaging
- [ ] Feedback rating system (1-5 stars)

### Analytics
- [ ] Complaint trends over time (day/week/month)
- [ ] Time-to-resolution metrics (median, mean)
- [ ] Department/campus heatmap
- [ ] CSV export for analytics
- [ ] Filtering by date range, category, department

### UI/UX
- [ ] Modern dashboard with cards and charts
- [ ] Responsive design
- [ ] Role-based dashboards (7 roles)
- [ ] Multi-language (English + Amharic)
- [ ] Dark/light mode
- [ ] PWA with offline support
- [ ] Toast notifications

### Security
- [ ] Input validation (server-side)
- [ ] SQL injection protection (ORM)
- [ ] XSS protection (output encoding)
- [ ] Password hashing (Argon2)
- [ ] Rate limiting on critical endpoints
- [ ] Activity logging
- [ ] File upload validation
- [ ] Authenticated file serving

### Documentation
- [ ] README.md with setup instructions
- [ ] .env.example
- [ ] API documentation (Swagger)
- [ ] ER diagram
- [ ] UML diagrams (use case, sequence)
- [ ] User manual (PDF)
- [ ] Project report (PDF)
- [ ] Demo script

### Testing
- [ ] Backend unit tests
- [ ] Backend integration tests
- [ ] Frontend unit tests
- [ ] Frontend E2E tests
- [ ] Seed data with test accounts

### Sample Accounts
- [ ] student@example.com / Student123! (Student)
- [ ] staff@example.com / Staff123! (Academic Staff)
- [ ] nonstaff@example.com / NonStaff123! (Non-academic Staff)
- [ ] maint@example.com / Maint123! (Maintenance Worker)
- [ ] depthead@example.com / DeptHead123! (Department Head)
- [ ] admin@example.com / Admin123! (System Admin)
- [ ] super@example.com / Super123! (Super Admin)

---

## Risk Management

### High Risk Items
1. **OAuth Integration** - May require UoG-specific configuration
   - Mitigation: Implement generic OAuth2 with clear placeholder docs
2. **Email Delivery** - SMTP configuration may fail
   - Mitigation: Use Mailtrap for testing, provide clear setup docs
3. **PWA Offline Sync** - Complex implementation
   - Mitigation: Start with basic offline draft storage, iterate
4. **Time Constraints** - 19 days is tight for full implementation
   - Mitigation: Prioritize core features, mark optional features clearly

### Medium Risk Items
1. **Database Migrations** - Schema changes may cause data loss
   - Mitigation: Backup database before migrations, test thoroughly
2. **Multi-language** - Amharic translation may be incomplete
   - Mitigation: Provide translation keys, use placeholders
3. **Analytics Performance** - Large datasets may slow queries
   - Mitigation: Add database indexes, implement caching

---

## Success Metrics

- ✅ All acceptance criteria met
- ✅ Test coverage > 70%
- ✅ All documentation complete
- ✅ Demo runs successfully in < 10 minutes
- ✅ No critical security vulnerabilities
- ✅ Code passes linting
- ✅ Application runs on localhost without errors

---

**Roadmap Version:** 1.0  
**Last Updated:** November 28, 2025
