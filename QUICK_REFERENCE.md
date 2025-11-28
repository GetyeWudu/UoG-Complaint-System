# Quick Reference Card - UoG Complaint System

## 🚀 Start System (2 Commands)

```bash
# Terminal 1 - Backend
cd backend && .\venv\Scripts\activate && python manage.py runserver

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

**URLs:**
- Frontend: http://localhost:5174
- Backend: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

---

## 👥 Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Student | student@uog.edu.et | student123 |
| Admin | admin@uog.edu.et | admin123 |
| Dept Head | depthead@uog.edu.et | dept123 |
| Proctor | proctor@uog.edu.et | proctor123 |

---

## 📧 Email Notifications (6 Types)

1. **Reviewed** - Admin looked at complaint
2. **Assigned** - Given to staff
3. **In Progress** - Being worked on
4. **Resolved** - Issue fixed
5. **Rejected** - Cannot process
6. **Closed** - Complete

**See emails in:** Backend console (development mode)

---

## 🔍 Key Features

- ✅ Submit complaints with files
- ✅ Track by ID
- ✅ Email notifications
- ✅ Search & filter
- ✅ Add comments
- ✅ Activity timeline
- ✅ Real-time updates (30s)
- ✅ Bell notifications

---

## 📚 Essential Docs

| Need | Read |
|------|------|
| Find any doc | [INDEX.md](INDEX.md) |
| Quick setup | [QUICK_START.md](QUICK_START.md) |
| Test features | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Admin tasks | [ADMIN_GUIDE.md](ADMIN_GUIDE.md) |
| Deploy | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) |
| Understand emails | [NOTIFICATION_GUIDE.md](NOTIFICATION_GUIDE.md) |

---

## 🐛 Common Issues

**Empty screen on create complaint?**
→ Fixed! Refresh page.

**Comment not posting?**
→ Fixed! Try again.

**Email not sending?**
→ Check backend console (dev mode)

**Can't login?**
→ Use test accounts above

---

## 🎯 Quick Test (5 min)

1. Login as student
2. Create complaint
3. Logout, login as admin
4. Change status to "assigned"
5. Check backend console for email
6. Login as student - see notification

---

## 📞 Help

**Stuck?** → [INDEX.md](INDEX.md)  
**Testing?** → [TESTING_GUIDE.md](TESTING_GUIDE.md)  
**Deploying?** → [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## ✅ Status: COMPLETE

**Version:** 1.0.0  
**Date:** Nov 28, 2025  
**Ready:** ✅ Production Ready

🎉 **All features working!**
