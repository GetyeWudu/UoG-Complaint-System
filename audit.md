# UoG Complaint Management System - Repository Audit

**Date:** November 28, 2025  
**Branch:** feature/complete-final-project  
**Auditor:** Kiro AI

---

## 1. Project Overview

### Tech Stack
- **Backend:** Django 5.0+ with Django REST Framework
- **Frontend:** React 19.2 with Vite, TailwindCSS, Recharts
- **Database:** SQLite3 (development)
- **Authentication:** Token-based (Django REST Framework Token Auth)
- **File Storage:** Local filesystem (evidence uploads)

### Current Structure
```
backend/
├── accounts/          # User management (CustomUser model)
├── complaints/        # Core complaint system
├── config/           # Django settings & main URLs
├── evidence/         # Uploaded files directory
└── db.sqlite3        # SQLite database

frontend/
├── src/
│   ├── App.jsx       # Main app component
│   ├── Dashboard.jsx # Role-based dashboard
│   ├── Login.jsx     # Authentication UI
│   └── api.js        # Axios configuration
└── public/           # Static assets (UoG logo)
```

---

## 2. Current Dependencies

### Backend (requirements.txt)
```
django>=5.0
djangorestframework
django-cors-headers
openai
```

**Missing Critical Dependencies:**
- `Pillow` - for image upload handling
- `textblob` - used in ai_service.py but not listed
- `python-decouple` - for environment variable management
- `django-ratelimit` - for rate limiting
- `pyotp` - for 2FA/TOTP implementation
- `qrcode` - for 2FA QR code generation
- `argon2-cffi` - for password hashing
- `drf-yasg` or `drf-spectacular` - for OpenAPI/Swagger docs
- `celery` - for async email tasks (optional but recommended)
- `django-filter` - for advanced filtering

### Frontend (package.json)
Current dependencies are adequate. May need to add:
- `chart.js` or keep `recharts` (already present)
- `react-toastify` - for better notifications
- `date-fns` - for date formatting
- Workbox/PWA plugins for offline support

---

## 3. Database Schema Overview

### Existing Tables

#### accounts_customuser
- Extends Django's AbstractUser
- Fields: `id`, `username`, `password`, `email`, `role`, `uog_id`, `telegram_chat_id`, `department_id`, `campus_id`
- Roles: student, academic, proctor, dept_head, dean, maintenance, admin
- **Missing:** Super Admin role, OAuth fields, 2FA fields, password reset tokens

#### accounts_campus
- Fields: `id`, `name`, `director_id`
- Represents physical campuses (Tewodros, Maraki, CMHS)

#### accounts_college
- Fields: `id`, `name`, `campus_id`, `dean_id`
- Represents colleges within campuses

#### accounts_department
- Fields: `id`, `name`, `college_id`, `head_id`
- Represents departments within colleges

#### complaints_complaint
- Fields: `id`, `tracking_id`, `title`, `description`, `location`, `image`, `is_academic`, `is_facility`, `urgency`, `status`, `user_id`, `assigned_to_id`, `created_at`, `feedback_rating`, `feedback_comment`
- Status values: open, pending_proctor, escalated, in_progress, resolved
- **Missing:** priority field, sub_category, closed_at, updated_at

#### complaints_userprofile
- Duplicate/redundant with CustomUser
- Fields: `id`, `user_id`, `is_student`, `is_staff`, `is_dept_head`, `campus`, `department`
- **Issue:** Overlaps with CustomUser model - needs consolidation

### Missing Tables (Required)
1. **complaint_events** - Audit trail for status changes
2. **complaint_comments** - Threaded messaging system
3. **complaint_files** - Multiple file attachments per complaint
4. **routing_rules** - Auto-assignment configuration
5. **email_templates** - Templated notifications
6. **activity_logs** - System-wide audit logs
7. **oauth_accounts** - OAuth account linking
8. **totp_devices** - 2FA device management
9. **password_reset_tokens** - Secure password reset
10. **categories** - Dynamic complaint categories
11. **offline_drafts** - PWA offline storage sync

---

## 4. Current Authentication Flow

### Implementation
- Token-based authentication using DRF's TokenAuthentication
- Login endpoint: `POST /api/login/` returns token + user info
- Token stored in localStorage on frontend
- Axios interceptor adds token to all requests

### What's Missing
1. **OAuth2 Integration:** No university SSO/OAuth flow
2. **Account Linking:** Cannot link local account to OAuth
3. **2FA/TOTP:** No two-factor authentication
4. **Password Reset:** No email-based password reset flow
5. **Registration:** No user registration endpoint
6. **Session Management:** No token expiry/refresh mechanism
7. **Rate Limiting:** No protection against brute force attacks

### Where to Plug OAuth
- Create new view: `OAuthCallbackView` in `accounts/views.py`
- Add OAuth provider config in settings (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
- Create `OAuthAccount` model to link OAuth ID to CustomUser
- Add OAuth button in Login.jsx with redirect to provider

---

## 5. File Upload Implementation

### Current State
- Single image upload per complaint via `ImageField`
- Stored in `backend/evidence/` directory
- Field name: `image` in Complaint model
- Frontend sends via FormData with multipart/form-data

### Issues & Gaps
1. **No validation:** Missing server-side file type/size validation
2. **Single file only:** Cannot upload multiple evidence files
3. **No metadata tracking:** No separate Files table
4. **Security risk:** Files may be directly accessible without auth
5. **No file serving endpoint:** Should use authenticated file serving
6. **Missing MEDIA_URL/MEDIA_ROOT:** Not configured in settings.py

### Required Changes
1. Add MEDIA_URL and MEDIA_ROOT to settings.py
2. Create separate `ComplaintFile` model
3. Implement file validation (max 10MB, allowed types: jpg, jpeg, png, gif, pdf)
4. Create authenticated file serving view
5. Support multiple file uploads per complaint

---

## 6. Existing Tests

**Status:** ❌ No tests found

### Missing Test Coverage
- Unit tests for models
- Unit tests for serializers
- Integration tests for API endpoints
- Authentication flow tests
- File upload tests
- Permission/RBAC tests
- Frontend component tests
- E2E tests

---

## 7. Current API Endpoints

### Authenticated Endpoints
- `POST /api/login/` - User login
- `GET /api/complaints/` - List complaints (role-filtered)
- `POST /api/complaints/` - Create complaint
- `GET /api/complaints/{id}/` - Retrieve complaint
- `PATCH /api/complaints/{id}/` - Update complaint
- `DELETE /api/complaints/{id}/` - Delete complaint
- `PATCH /api/complaints/{id}/feedback/` - Submit feedback

### Public Endpoints
- `POST /api/public/submit/` - Anonymous complaint submission
- `GET /api/public/track/{tracking_id}/` - Track complaint by token

### Missing Endpoints
- User registration
- Password reset (request & confirm)
- OAuth callback
- 2FA setup/verify
- Staff listing (exists but not in main urls)
- Assignment endpoints
- Comments/messaging
- File upload/download
- Analytics endpoints (trends, time-to-resolution, heatmap)
- Category management
- Routing rules management
- Activity logs
- CSV/PDF export

---

## 8. Role-Based Access Control (RBAC)

### Current Implementation
- Roles defined in CustomUser.ROLE_CHOICES
- View-level filtering in `ComplaintListCreateView.get_queryset()`
- Basic role checks in frontend Dashboard

### Current Roles
1. **student** - Can create and view own complaints
2. **academic** - Academic staff (no specific permissions yet)
3. **proctor** - Can view/manage facility complaints
4. **dept_head** - Can view academic complaints in their department
5. **dean** - College dean (no specific permissions yet)
6. **maintenance** - Maintenance worker (no specific permissions yet)
7. **admin** - System admin (can see all complaints)

### Missing
- **Super Admin** role (required by spec)
- **Non-academic Staff** role (required by spec)
- Permission-based access control (not just role checks)
- Assignment permissions
- Department-level restrictions for staff
- Approval workflows

---

## 9. AI Service Analysis

### Current Implementation
- File: `complaints/ai_service.py`
- Function: `analyze_urgency(text)` returns 'high', 'medium', or 'low'
- Method: Keyword matching + sentiment analysis using TextBlob
- **Issue:** Uses TextBlob but not in requirements.txt
- **Issue:** requirements.txt includes `openai` but it's not used

### Recommendations
- Add `textblob` to requirements.txt
- Remove unused `openai` dependency or implement GPT-based analysis
- Enhance keyword list for better accuracy
- Add category detection capability

---

## 10. Frontend Analysis

### Current State
- Modern React app with TailwindCSS
- Role-based dashboard with conditional rendering
- Charts using Recharts (Pie, Bar)
- Responsive design
- Token-based auth with localStorage

### Strengths
- Clean UI with UoG branding
- Good separation of concerns
- Axios interceptor for auth
- Basic analytics visualization

### Gaps
1. **No routing:** Uses view state instead of React Router (though package is installed)
2. **No multi-language:** English only, no Amharic support
3. **No dark mode:** Not implemented
4. **No PWA:** No service worker or offline support
5. **No error boundaries:** No graceful error handling
6. **No loading states:** Limited loading indicators
7. **No form validation:** Client-side validation missing
8. **No file preview:** Cannot preview uploaded images before submit
9. **No real-time updates:** No WebSocket or polling
10. **No export functionality:** Cannot export data to PDF/CSV

---

## 11. Security Assessment

### Current Security Measures ✅
- Token-based authentication
- CORS configured (though set to allow all origins)
- Django's built-in CSRF protection
- Password hashing (Django default PBKDF2)

### Critical Security Gaps ❌
1. **SQL Injection:** Using ORM (safe), but no explicit validation
2. **XSS Protection:** No output encoding in frontend
3. **Rate Limiting:** None implemented
4. **Password Strength:** No validation rules
5. **File Upload Security:** No validation, potential RCE risk
6. **HTTPS:** Not configured (acceptable for localhost)
7. **Secrets Management:** SECRET_KEY hardcoded in settings.py
8. **CORS:** Set to allow all origins (insecure)
9. **Activity Logging:** No audit trail
10. **Input Validation:** Minimal server-side validation

---

## 12. Email System

### Current State
**Status:** ❌ Not implemented

### Required
- SMTP configuration in settings
- Email backend setup
- HTML + text email templates
- Notification triggers:
  - Complaint submission confirmation
  - Assignment notification
  - Status change notification
  - Resolution notification
  - Password reset
  - 2FA codes (optional)

---

## 13. Analytics & Reporting

### Current State
- Basic frontend charts (status pie chart, type bar chart)
- No backend analytics endpoints
- No time-series analysis
- No heatmap data
- No export functionality

### Required
- Trends over time (day/week/month)
- Time-to-resolution metrics (median, mean, distribution)
- Department/campus heatmap data
- CSV/PDF export
- Filtering by date range, category, department

---

## 14. Documentation

### Existing
- Basic README.md in frontend (Vite boilerplate)
- No API documentation
- No setup instructions
- No user manual
- No architecture diagrams

### Required
- Comprehensive README.md with setup steps
- .env.example file
- API documentation (OpenAPI/Swagger)
- ER diagram
- UML diagrams (use case, sequence)
- User manual (PDF)
- Project report (PDF)
- Demo script

---

## 15. Critical Issues Summary

### High Priority 🔴
1. Add missing dependencies to requirements.txt
2. Consolidate UserProfile and CustomUser models
3. Implement file upload validation (security risk)
4. Add MEDIA_URL/MEDIA_ROOT configuration
5. Create missing database tables (audit trail, comments, files)
6. Implement rate limiting (security risk)
7. Add input validation (security risk)
8. Configure proper CORS settings

### Medium Priority 🟡
1. Add Super Admin and Non-academic Staff roles
2. Implement OAuth2 integration
3. Add 2FA/TOTP support
4. Create email notification system
5. Build analytics endpoints
6. Add comprehensive tests
7. Implement PWA offline support
8. Add multi-language support

### Low Priority 🟢
1. Add dark mode
2. Implement real-time updates
3. Add advanced filtering
4. Create admin settings UI
5. Add export to PDF functionality

---

## 16. Recommended Refactoring

### Backend
1. **Consolidate user models:** Merge UserProfile into CustomUser
2. **Add services layer:** Separate business logic from views
3. **Create permissions classes:** Implement DRF permissions for RBAC
4. **Add serializer validation:** Implement field-level validation
5. **Use environment variables:** Move secrets to .env file
6. **Add logging:** Implement structured logging
7. **Create management commands:** For seeding data, creating users

### Frontend
1. **Implement React Router:** Replace view state with proper routing
2. **Add context/state management:** Consider Context API or Zustand
3. **Create reusable components:** Extract common UI elements
4. **Add form validation:** Use a library like react-hook-form
5. **Implement error boundaries:** Graceful error handling
6. **Add loading states:** Better UX during API calls
7. **Create translation files:** i18n setup for multi-language

---

## 17. Estimated Effort

### Phase 1: Backend Core (5-7 days)
- Database migrations
- Authentication enhancements
- File upload system
- Email notifications
- API endpoints
- Security hardening

### Phase 2: Frontend (4-5 days)
- Dashboard improvements
- Multi-language support
- PWA implementation
- Charts and analytics
- Form validation

### Phase 3: Analytics & Reporting (2-3 days)
- Analytics endpoints
- Export functionality
- Advanced visualizations

### Phase 4: Tests & Documentation (3-4 days)
- Unit and integration tests
- API documentation
- Diagrams
- User manual
- Project report

**Total Estimated Time:** 14-19 days

---

## 18. Next Steps

1. ✅ Create feature branch
2. ✅ Complete audit document
3. ⏳ Create ROADMAP.md with detailed milestones
4. ⏳ Update requirements.txt with missing dependencies
5. ⏳ Create .env.example file
6. ⏳ Begin Phase 1 implementation

---

**Audit Complete** ✅
