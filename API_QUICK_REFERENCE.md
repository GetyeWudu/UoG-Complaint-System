# API Quick Reference - UoG Complaint Management System

**Base URL:** `http://127.0.0.1:8000/api/`  
**Authentication:** Token-based (include `Authorization: Token <your-token>` header)

---

## 🔐 Authentication Endpoints

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "TestPass123!",
  "password_confirm": "TestPass123!",
  "first_name": "Test",
  "last_name": "User",
  "role": "student"
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "student@example.com",
  "password": "Student123!"
}

Response:
{
  "token": "abc123...",
  "user_id": 1,
  "username": "student@example.com",
  "role": "student",
  ...
}
```

### Logout
```http
POST /api/auth/logout/
Authorization: Token <your-token>
```

### Password Reset Request
```http
POST /api/auth/password-reset/request/
Content-Type: application/json

{
  "email": "student@example.com"
}
```

### Password Reset Confirm
```http
POST /api/auth/password-reset/confirm/
Content-Type: application/json

{
  "token": "reset-token-from-email",
  "password": "NewPass123!",
  "password_confirm": "NewPass123!"
}
```

### Get Current User
```http
GET /api/auth/me/
Authorization: Token <your-token>
```

---

## 📝 Complaint Endpoints

### List Complaints
```http
GET /api/complaints/
Authorization: Token <your-token>

# Returns complaints based on user role:
# - Student: own complaints
# - Staff: assigned complaints
# - Dept Head: department complaints
# - Admin: all complaints
```

### Create Complaint
```http
POST /api/complaints/
Authorization: Token <your-token>
Content-Type: multipart/form-data

{
  "title": "Broken projector in Room 301",
  "description": "The projector is not working",
  "location": "Tewodros Campus, Room 301",
  "category": 1,
  "sub_category": 2,
  "campus": 1,
  "uploaded_files": [file1, file2]  // Optional
}
```

### Get Complaint Details
```http
GET /api/complaints/{id}/
Authorization: Token <your-token>

# Returns full complaint with files, comments, and events
```

### Update Complaint
```http
PATCH /api/complaints/{id}/
Authorization: Token <your-token>
Content-Type: application/json

{
  "description": "Updated description",
  "priority": "high"
}
```

### Assign Complaint
```http
POST /api/complaints/{id}/assign/
Authorization: Token <your-token>
Content-Type: application/json

{
  "assigned_to": 5  // User ID
}

# Requires: dept_head, admin, or super_admin role
```

### Update Status
```http
POST /api/complaints/{id}/status/
Authorization: Token <your-token>
Content-Type: application/json

{
  "status": "in_progress",
  "notes": "Started working on this issue"
}

# Valid statuses: new, assigned, in_progress, pending, resolved, closed, rejected
```

### Submit Feedback
```http
PATCH /api/complaints/{id}/feedback/
Authorization: Token <your-token>
Content-Type: application/json

{
  "feedback_rating": 5,
  "feedback_comment": "Great service!"
}
```

---

## 📎 File Management

### Upload Files
```http
POST /api/complaints/{complaint_id}/files/
Authorization: Token <your-token>
Content-Type: multipart/form-data

files: [file1, file2, file3]

# Max 10MB per file
# Allowed types: jpg, jpeg, png, gif, pdf
```

### Download File
```http
GET /api/complaints/files/{file_id}/download/
Authorization: Token <your-token>

# Returns file with proper Content-Type and Content-Disposition headers
```

### Delete File
```http
DELETE /api/complaints/files/{file_id}/
Authorization: Token <your-token>

# Only uploader or admin can delete
```

---

## 💬 Comments

### List Comments
```http
GET /api/complaints/{complaint_id}/comments/
Authorization: Token <your-token>

# Returns top-level comments with nested replies
```

### Add Comment
```http
POST /api/complaints/{complaint_id}/comments/
Authorization: Token <your-token>
Content-Type: application/json

{
  "content": "This is my comment",
  "parent": null,  // Or parent comment ID for replies
  "is_internal": false  // true for staff-only notes
}
```

---

## 🌍 Public Endpoints (No Auth Required)

### Anonymous Complaint Submission
```http
POST /api/public/submit/
Content-Type: application/json

{
  "title": "Issue title",
  "description": "Issue description",
  "location": "Location details"
}

Response:
{
  "tracking_id": "CMP-ABC123",
  "message": "Submitted!"
}
```

### Track Complaint
```http
GET /api/public/track/{tracking_id}/

Response:
{
  "title": "Issue title",
  "status": "new",
  "urgency": "medium",
  "location": "Location",
  "created_at": "2025-11-28T10:00:00Z"
}
```

---

## 🏢 Utility Endpoints

### List Campuses
```http
GET /api/auth/campuses/

Response:
[
  {"id": 1, "name": "Tewodros Campus"},
  {"id": 2, "name": "Maraki Campus"},
  {"id": 3, "name": "CMHS Campus"}
]
```

### List Departments
```http
GET /api/auth/departments/

Response:
[
  {
    "id": 1,
    "name": "Computer Science",
    "college_name": "College of Informatics",
    "campus_name": "Tewodros Campus"
  },
  ...
]
```

### List Staff
```http
GET /api/complaints/staff/
Authorization: Token <your-token>

# Returns all non-student users
```

### Activity Logs
```http
GET /api/auth/activity-logs/
Authorization: Token <your-token>

# Users see own logs
# Admins see all logs
```

---

## 📖 API Documentation

### Swagger UI (Interactive)
```
http://127.0.0.1:8000/api/docs/
```

### ReDoc (Documentation)
```
http://127.0.0.1:8000/api/redoc/
```

### OpenAPI Schema (JSON)
```
http://127.0.0.1:8000/api/schema/
```

---

## 🔑 Test Accounts

| Email | Password | Role |
|-------|----------|------|
| student@example.com | Student123! | Student |
| staff@example.com | Staff123! | Academic Staff |
| nonstaff@example.com | NonStaff123! | Non-academic Staff |
| maint@example.com | Maint123! | Maintenance Worker |
| depthead@example.com | DeptHead123! | Department Head |
| admin@example.com | Admin123! | System Admin |
| super@example.com | Super123! | Super Admin |

---

## 🚨 Error Responses

### 400 Bad Request
```json
{
  "error": "Validation error message",
  "field_name": ["Error detail"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "Permission denied"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

---

## 📊 Response Formats

### Complaint Object
```json
{
  "id": 1,
  "tracking_id": "CMP-ABC12345",
  "title": "Issue title",
  "description": "Issue description",
  "category": 1,
  "category_name": "Facility",
  "sub_category": 2,
  "sub_category_name": "Classroom Maintenance",
  "campus": 1,
  "campus_name": "Tewodros Campus",
  "department": 1,
  "department_name": "Computer Science",
  "location": "Room 301",
  "status": "new",
  "priority": "medium",
  "urgency": "high",
  "submitter": 1,
  "submitter_username": "student@example.com",
  "submitter_name": "Test Student",
  "assigned_to": null,
  "is_anonymous": false,
  "created_at": "2025-11-28T10:00:00Z",
  "updated_at": "2025-11-28T10:00:00Z",
  "files": [
    {
      "id": 1,
      "filename": "evidence.jpg",
      "file_size": 102400,
      "file_url": "/api/complaints/files/1/download/",
      "uploaded_at": "2025-11-28T10:00:00Z"
    }
  ],
  "comments": [
    {
      "id": 1,
      "author_username": "staff@example.com",
      "author_name": "Staff Member",
      "content": "Working on this",
      "created_at": "2025-11-28T11:00:00Z",
      "replies": []
    }
  ],
  "events": [
    {
      "id": 1,
      "event_type": "created",
      "event_type_display": "Created",
      "actor_username": "student@example.com",
      "timestamp": "2025-11-28T10:00:00Z"
    }
  ]
}
```

---

## 🧪 Testing with cURL

### Login and Save Token
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student@example.com","password":"Student123!"}' \
  | jq -r '.token' > token.txt

# Use token
TOKEN=$(cat token.txt)
```

### Create Complaint
```bash
curl -X POST http://127.0.0.1:8000/api/complaints/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Complaint",
    "description": "This is a test",
    "location": "Test Location",
    "category": 1
  }'
```

### Upload File
```bash
curl -X POST http://127.0.0.1:8000/api/complaints/1/files/ \
  -H "Authorization: Token $TOKEN" \
  -F "files=@/path/to/file.jpg"
```

---

## 💡 Tips

1. **Use Swagger UI** for interactive testing: http://127.0.0.1:8000/api/docs/
2. **Check Activity Logs** to debug auth issues
3. **Use tracking_id** for anonymous complaint tracking
4. **File uploads** support multiple files in one request
5. **Comments** support threading (use parent field for replies)
6. **Status transitions** are validated server-side
7. **Auto-routing** applies on complaint creation
8. **Email notifications** sent automatically on key events

---

**For detailed documentation, visit:** http://127.0.0.1:8000/api/docs/
