# Notification System Guide

## When Admin Reviews a Complaint

### What the Student Sees

#### 1. Email Notification (Immediate)
```
From: UoG Complaints <noreply@uog.edu.et>
To: student@uog.edu.et
Subject: Your Complaint Has Been Reviewed - CMP-ABC12345

Dear John Doe,

Your complaint has been reviewed by our team.

Complaint Details:
- Tracking ID: CMP-ABC12345
- Title: Broken AC in Library
- Status: Assigned
- Priority: High

Our team has reviewed your complaint and will take appropriate action.

You can track your complaint status at any time using your tracking ID.

Best regards,
UoG Complaint Management Team
```

#### 2. In-App Notification (Dashboard)
- **Bell icon** in header shows red badge with number
- Click bell to see dropdown:
  ```
  Recent Activity
  ─────────────────────────────────
  Status changed from new to assigned
  Nov 28, 2025, 2:30 PM
  
  Complaint CMP-ABC12345 was reviewed
  Nov 28, 2025, 2:30 PM
  ```

#### 3. Dashboard Update
- Complaint card shows updated status badge
- Status changes from "NEW" (blue) to "ASSIGNED" (purple)
- Last updated timestamp refreshes

#### 4. Complaint Detail Page
- Activity Timeline shows new entry:
  ```
  Activity Timeline
  ─────────────────────────────────
  │ Status changed from new to assigned
  │ Nov 28, 2025, 2:30 PM • by Admin User
  │
  │ Complaint created
  │ Nov 28, 2025, 1:00 PM • by John Doe
  ```

## All Notification Types

### 1. Complaint Reviewed (Initial Review)
**Trigger**: Admin first looks at and processes the complaint

**Email Subject**: `Your Complaint Has Been Reviewed - {tracking_id}`

**Message**:
- Confirms complaint was reviewed
- Shows current status and priority
- Reassures student action will be taken

**When**: Immediately after admin changes status from "new"

---

### 2. Complaint Assigned
**Trigger**: Admin assigns complaint to a staff member

**Email Subject**: `Your Complaint Has Been Assigned - {tracking_id}`

**Message**:
- Shows who the complaint was assigned to
- Indicates work will begin soon
- Provides tracking information

**When**: Status changes to "assigned"

---

### 3. In Progress
**Trigger**: Staff member starts working on the complaint

**Email Subject**: `Your Complaint is Being Processed - {tracking_id}`

**Message**:
- Confirms active work is happening
- Shows assigned staff member
- Sets expectation for resolution

**When**: Status changes to "in_progress"

---

### 4. Resolved
**Trigger**: Complaint is marked as resolved

**Email Subject**: `Your Complaint Has Been Resolved - {tracking_id}`

**Message**:
- Celebrates resolution
- Includes resolution notes
- Asks for feedback (optional)

**When**: Status changes to "resolved"

**Example**:
```
Dear John Doe,

Great news! Your complaint has been resolved.

Complaint Details:
- Tracking ID: CMP-ABC12345
- Title: Broken AC in Library
- Status: Resolved
- Resolution Notes: AC unit has been repaired and is now functioning properly. 
  Maintenance team tested it and confirmed it's working at optimal temperature.

If you are satisfied with the resolution, no further action is needed.
If you have any concerns, please contact us.

Best regards,
UoG Complaint Management Team
```

---

### 5. Rejected
**Trigger**: Complaint cannot be processed

**Email Subject**: `Complaint Status Update - {tracking_id}`

**Message**:
- Explains complaint was rejected
- Provides clear reason
- Offers contact information for questions

**When**: Status changes to "rejected"

**Example**:
```
Dear John Doe,

We have reviewed your complaint and unfortunately cannot proceed with it at this time.

Complaint Details:
- Tracking ID: CMP-ABC12345
- Title: Request for New Building
- Status: Rejected
- Reason: This request falls outside the scope of the complaint system. 
  Please submit facility requests through the proper channels at facilities@uog.edu.et

If you have questions about this decision, please contact our support team.

Best regards,
UoG Complaint Management Team
```

---

### 6. Closed
**Trigger**: Complaint is officially closed

**Email Subject**: `Your Complaint Has Been Closed - {tracking_id}`

**Message**:
- Confirms closure
- Summarizes final resolution
- Thanks student for using system

**When**: Status changes to "closed"

---

## Notification Delivery

### Email Delivery
- **Immediate**: Sent as soon as status changes
- **Reliable**: Uses Django's email system
- **Formatted**: Clean, professional HTML emails
- **Trackable**: Logged in system for audit

### In-App Notifications
- **Real-time**: Updates every 30 seconds
- **Persistent**: Stored in activity log
- **Accessible**: Available in notification dropdown
- **Historical**: Can view past notifications

## Admin Actions That Trigger Notifications

| Admin Action | Notification Sent | Email Type |
|-------------|-------------------|------------|
| Change status to "assigned" | ✅ Yes | Complaint Assigned |
| Change status to "in_progress" | ✅ Yes | In Progress |
| Change status to "resolved" | ✅ Yes | Resolved |
| Change status to "rejected" | ✅ Yes | Rejected |
| Change status to "closed" | ✅ Yes | Closed |
| Add comment | ❌ No | - |
| Upload file | ❌ No | - |
| Update priority | ❌ No | - |
| Assign to different staff | ✅ Yes | Complaint Assigned |

## Testing Notifications

### Development Mode (Console)
1. Set in `backend/.env`:
   ```
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

2. Watch backend console when status changes:
   ```
   Content-Type: text/plain; charset="utf-8"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   Subject: Your Complaint Has Been Reviewed - CMP-ABC12345
   From: UoG Complaints <noreply@uog.edu.et>
   To: student@uog.edu.et
   Date: Thu, 28 Nov 2025 14:30:00 -0000
   
   Dear John Doe,
   
   Your complaint has been reviewed by our team...
   ```

### Production Mode (Real Email)
1. Configure SMTP in `backend/.env`:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=UoG Complaints <your-email@gmail.com>
   ```

2. Test with real email address

### Gmail Setup (for testing)
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate App Password
4. Use App Password in EMAIL_HOST_PASSWORD

## Customizing Notifications

### Change Email Content
Edit `backend/complaints/notifications.py`:

```python
templates = {
    'reviewed': {
        'subject': 'Your Custom Subject - {tracking_id}',
        'message': '''
Your custom message here...
        '''
    }
}
```

### Add New Notification Type
1. Add template to `notifications.py`
2. Create notification function
3. Call from view when needed

### Disable Notifications
Comment out notification calls in `backend/complaints/views.py`:

```python
# notify_complaint_assigned(complaint)  # Disabled
```

## Notification Best Practices

### For Admins
1. **Update status promptly** - Students are waiting
2. **Add resolution notes** - Helps students understand outcome
3. **Be clear in rejection reasons** - Explain why and what to do next
4. **Assign quickly** - Don't leave complaints in "new" status

### For System Administrators
1. **Monitor email delivery** - Check for bounces
2. **Keep templates updated** - Match your institution's tone
3. **Test regularly** - Ensure notifications work
4. **Log everything** - Track notification history

## Troubleshooting

### Emails Not Sending
1. Check EMAIL_BACKEND setting
2. Verify SMTP credentials
3. Check spam folder
4. Review Django logs for errors
5. Test with console backend first

### Notifications Not Appearing
1. Check browser console for errors
2. Verify API endpoint is accessible
3. Check user permissions
4. Refresh page manually

### Wrong Email Content
1. Check template in notifications.py
2. Verify context variables
3. Test with different complaint types
4. Review email logs

## Future Enhancements

### Planned Features
- [ ] SMS notifications
- [ ] Push notifications (mobile app)
- [ ] Notification preferences (email/SMS/push)
- [ ] Digest emails (daily summary)
- [ ] Notification history page
- [ ] Mark notifications as read
- [ ] Notification sound/badge
- [ ] Custom notification templates per user role

### Integration Ideas
- Slack/Teams integration for staff
- WhatsApp notifications
- Mobile app with push notifications
- Browser push notifications
- Telegram bot integration
