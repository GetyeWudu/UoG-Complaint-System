# Administrator Guide - UoG Complaint Management System

## Admin Dashboard Overview

As an administrator, you have full access to all complaints and system features.

### Login Credentials
- **Email**: admin@uog.edu.et
- **Password**: admin123 (Change this immediately!)

## Daily Tasks

### 1. Review New Complaints

**Morning Routine:**
1. Login to dashboard
2. Check "New" complaints count in stats
3. Click on each new complaint
4. Assess urgency and category
5. Assign to appropriate staff member
6. Change status to "Assigned"

**What Happens:**
- Student receives email notification
- Assigned staff member can see the complaint
- Activity log records the assignment

### 2. Monitor In-Progress Complaints

**Check Progress:**
1. Filter by "In Progress" status
2. Review each complaint
3. Check if staff needs help
4. Add comments if needed
5. Follow up on delayed complaints

**Red Flags:**
- Complaints open > 7 days
- No comments from assigned staff
- High priority not progressing

### 3. Resolve Complaints

**Resolution Process:**
1. Open complaint
2. Verify issue is fixed
3. Add resolution notes (detailed explanation)
4. Change status to "Resolved"
5. Student receives resolution email

**Good Resolution Notes:**
```
✅ Good: "The broken projector in Room 301 has been replaced with a new 
model. Maintenance team tested it and confirmed it's working properly. 
The room is now ready for use."

❌ Bad: "Fixed"
```

## Complaint Management

### Assigning Complaints

**Auto-Routing:**
The system automatically routes complaints based on rules:
- **Facility issues** → Proctor
- **Academic issues** → Department Head
- **General issues** → Admin review

**Manual Assignment:**
1. Open complaint
2. Click "Assign" or update assigned_to field
3. Select staff member from dropdown
4. Save changes
5. Staff member gets notification

### Status Workflow

```
New → Assigned → In Progress → Resolved → Closed
                              ↓
                          Rejected
```

**Status Meanings:**
- **New**: Just submitted, needs review
- **Assigned**: Given to staff member
- **In Progress**: Being worked on
- **Resolved**: Issue fixed, awaiting confirmation
- **Closed**: Completed and confirmed
- **Rejected**: Cannot be processed

### Priority Levels

**Setting Priority:**
- System auto-assigns based on AI analysis
- You can manually override

**Priority Guidelines:**
- **Critical**: Safety hazards, system outages
- **High**: Affects many students, urgent
- **Medium**: Standard issues
- **Low**: Minor inconveniences

## User Management

### Creating New Users

**Via Django Admin:**
1. Go to http://your-domain.com/admin
2. Login with superuser credentials
3. Click "Users" → "Add User"
4. Fill in details:
   - Username
   - Email
   - Password
   - Role (student, staff, admin, etc.)
   - Campus
   - Department (if applicable)
5. Save

**Via Command Line:**
```bash
python manage.py createsuperuser
```

### User Roles

| Role | Can Do | Cannot Do |
|------|--------|-----------|
| **Student** | Submit complaints, track status, add comments | View others' complaints, assign, resolve |
| **Proctor** | View facility complaints, update status | View academic complaints, delete |
| **Dept Head** | View department complaints, assign, resolve | View other departments, system settings |
| **Admin** | Everything except delete system data | - |
| **Super Admin** | Everything including system settings | - |

### Deactivating Users

1. Go to Django admin
2. Find user
3. Uncheck "Active" status
4. Save
5. User cannot login anymore

## Search and Filtering

### Finding Specific Complaints

**By Tracking ID:**
1. Use search bar
2. Type tracking ID (e.g., CMP-ABC12345)
3. Press Enter

**By Status:**
1. Click status filter dropdown
2. Select status
3. View filtered results

**By Priority:**
1. Click priority filter dropdown
2. Select priority level
3. View filtered results

**Combined Search:**
- Type keyword + select status + select priority
- All filters work together

### Advanced Filtering

**In Django Admin:**
- More filter options available
- Date ranges
- User filters
- Campus/Department filters

## Communication

### Adding Comments

**Internal Comments:**
- Check "Internal" checkbox
- Only staff can see
- Use for coordination

**Public Comments:**
- Visible to student
- Use for updates and questions
- Professional tone

**Comment Best Practices:**
```
✅ Good: "We've scheduled a technician to inspect the AC unit on 
Friday at 2 PM. We'll update you once the repair is complete."

❌ Bad: "ok"
```

### Email Notifications

**Automatic Emails Sent When:**
- Status changes to Assigned
- Status changes to In Progress
- Status changes to Resolved
- Status changes to Rejected
- Status changes to Closed

**Email Content:**
- Tracking ID
- Complaint title
- New status
- Resolution notes (if resolved)
- Rejection reason (if rejected)

**Checking Email Delivery:**
- Development: Check console output
- Production: Check email service logs

## Reporting

### Statistics Dashboard

**Available Metrics:**
- Total complaints
- New complaints
- In progress
- Resolved
- Average resolution time
- Complaints by category
- Complaints by campus

### Generating Reports

**Via Django Admin:**
1. Go to Complaints section
2. Select complaints
3. Choose "Export as CSV" action
4. Download file

**Custom Reports:**
```python
# In Django shell
from complaints.models import Complaint
from django.utils import timezone
from datetime import timedelta

# Complaints this month
this_month = Complaint.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=30)
)

# Resolution time
resolved = Complaint.objects.filter(status='resolved')
for c in resolved:
    if c.resolved_at:
        time_taken = c.resolved_at - c.created_at
        print(f"{c.tracking_id}: {time_taken.days} days")
```

## System Configuration

### Email Templates

**Location:** Django Admin → Email Templates

**Customizing:**
1. Find template (e.g., "complaint_assigned")
2. Edit subject and content
3. Use variables: {tracking_id}, {title}, {status}
4. Save changes

**Example Template:**
```
Subject: Complaint Update - {tracking_id}

Dear {submitter_name},

Your complaint "{title}" has been updated.

Status: {status}
Priority: {priority}

{additional_message}

Track your complaint: {complaint_url}

Best regards,
UoG Complaint Team
```

### Routing Rules

**Location:** Django Admin → Routing Rules

**Creating Rule:**
1. Click "Add Routing Rule"
2. Set conditions:
   - Keyword in title/description
   - Category
   - Campus
   - Priority
3. Set action:
   - Assign to specific user
   - Assign to role
   - Set priority
4. Set priority (order of execution)
5. Save

**Example Rules:**
```
Rule 1: If description contains "broken projector" → Assign to Facilities Team
Rule 2: If category is "Academic" → Assign to Department Head
Rule 3: If priority is "Critical" → Notify Super Admin
```

### Campus and Department Management

**Adding Campus:**
1. Django Admin → Campuses → Add
2. Enter name (e.g., "Tewodros Campus")
3. Save

**Adding Department:**
1. Django Admin → Departments → Add
2. Enter name
3. Select campus
4. Select college
5. Save

## Troubleshooting

### Common Issues

#### 1. Complaint Not Appearing
**Possible Causes:**
- Permission issue
- Filter applied
- Database sync issue

**Solution:**
1. Clear all filters
2. Refresh page
3. Check user permissions
4. Check database

#### 2. Email Not Sending
**Possible Causes:**
- SMTP configuration wrong
- Email service down
- Invalid recipient email

**Solution:**
1. Check EMAIL_BACKEND setting
2. Verify SMTP credentials
3. Check email service status
4. Test with console backend

#### 3. File Upload Failing
**Possible Causes:**
- File too large (>10MB)
- Invalid file type
- Storage full

**Solution:**
1. Check file size
2. Verify file extension
3. Check disk space
4. Review error logs

#### 4. Search Not Working
**Possible Causes:**
- Database index issue
- Special characters
- Case sensitivity

**Solution:**
1. Try different search terms
2. Use tracking ID instead
3. Check database indexes

### Checking Logs

**Backend Logs:**
```bash
# Heroku
heroku logs --tail

# Local
# Check console output

# Production
tail -f /var/log/complaints/error.log
```

**Frontend Logs:**
- Open browser console (F12)
- Check Network tab for API errors
- Look for red error messages

## Security

### Best Practices

1. **Change Default Passwords**
   - All admin accounts
   - Database passwords
   - Email passwords

2. **Regular Updates**
   - Update Django monthly
   - Update dependencies
   - Apply security patches

3. **Access Control**
   - Use strong passwords
   - Enable 2FA (if available)
   - Limit admin accounts
   - Review user permissions

4. **Data Protection**
   - Regular backups
   - Encrypt sensitive data
   - HTTPS only
   - Secure file uploads

### Handling Security Issues

**If Breach Suspected:**
1. Change all passwords immediately
2. Review access logs
3. Check for unauthorized changes
4. Notify users if needed
5. Document incident

**Prevention:**
- Monitor login attempts
- Review activity logs weekly
- Keep software updated
- Use strong passwords

## Performance Monitoring

### Key Metrics

**Response Time:**
- Target: < 500ms
- Check: Network tab in browser
- Improve: Add caching, optimize queries

**Database Performance:**
- Monitor query count
- Check slow queries
- Add indexes if needed

**Email Delivery:**
- Track bounce rate
- Monitor delivery time
- Check spam reports

### Optimization Tips

1. **Database:**
   - Regular VACUUM (PostgreSQL)
   - Add indexes on frequently searched fields
   - Archive old complaints

2. **Files:**
   - Compress images
   - Use CDN for static files
   - Clean up old files

3. **Caching:**
   - Enable Redis caching
   - Cache API responses
   - Use browser caching

## Backup and Recovery

### Backup Schedule

**Daily:**
- Database backup
- Media files backup

**Weekly:**
- Full system backup
- Configuration backup

**Monthly:**
- Archive old data
- Test restore procedure

### Restore Procedure

**Database Restore:**
```bash
# PostgreSQL
psql complaints_db < backup.sql

# Heroku
heroku pg:backups:restore
```

**Files Restore:**
```bash
# From S3
aws s3 sync s3://backup-bucket/media /path/to/media
```

## Maintenance Tasks

### Weekly
- [ ] Review new complaints
- [ ] Check email delivery
- [ ] Monitor error logs
- [ ] Update statistics

### Monthly
- [ ] Update dependencies
- [ ] Review user accounts
- [ ] Check disk space
- [ ] Generate reports
- [ ] Archive old complaints

### Quarterly
- [ ] Security audit
- [ ] Performance review
- [ ] User feedback review
- [ ] System optimization

### Yearly
- [ ] Major version updates
- [ ] Infrastructure review
- [ ] Disaster recovery test
- [ ] Policy review

## Training New Admins

### Onboarding Checklist

- [ ] Create admin account
- [ ] Tour of dashboard
- [ ] Explain complaint workflow
- [ ] Practice assigning complaints
- [ ] Practice resolving complaints
- [ ] Review email templates
- [ ] Show reporting features
- [ ] Explain security policies
- [ ] Provide documentation access

### Training Resources

1. **This Guide** - Complete admin reference
2. **TESTING_GUIDE.md** - How to test features
3. **API_QUICK_REFERENCE.md** - API documentation
4. **NOTIFICATION_GUIDE.md** - Email system details

## Support

### Getting Help

**Technical Issues:**
1. Check this guide
2. Review error logs
3. Search documentation
4. Contact system administrator

**User Issues:**
1. Check user permissions
2. Verify account status
3. Reset password if needed
4. Contact support team

### Escalation

**Level 1:** Admin handles
- User questions
- Basic troubleshooting
- Complaint management

**Level 2:** System Admin handles
- Technical issues
- Configuration changes
- Performance problems

**Level 3:** Developer handles
- Code bugs
- Feature requests
- System upgrades

## Quick Reference

### Keyboard Shortcuts
- `Ctrl + F`: Search
- `F5`: Refresh
- `Ctrl + Click`: Open in new tab

### Common URLs
- Dashboard: `/dashboard`
- Admin Panel: `/admin`
- API Docs: `/api/docs` (if enabled)

### Important Commands
```bash
# Create superuser
python manage.py createsuperuser

# Seed test data
python manage.py seed_data

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

### Contact Information
- **System Admin**: admin@uog.edu.et
- **Technical Support**: support@uog.edu.et
- **Emergency**: [Phone Number]

---

**Last Updated**: November 28, 2025
**Version**: 1.0.0
**Next Review**: December 28, 2025
