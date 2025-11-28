# Deployment Guide - UoG Complaint Management System

## Pre-Deployment Checklist

### ✅ Code Ready
- [x] All features implemented
- [x] Bugs fixed
- [x] Tests passing
- [x] Documentation complete

### ✅ Configuration
- [ ] Environment variables set
- [ ] Database configured
- [ ] Email service configured
- [ ] Static files configured
- [ ] CORS settings updated

### ✅ Security
- [ ] DEBUG=False
- [ ] SECRET_KEY changed
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Security headers added

## Deployment Options

### Option 1: Heroku (Recommended for Beginners)

#### Backend Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Prepare Backend**
   ```bash
   cd backend
   
   # Create Procfile
   echo "web: gunicorn config.wsgi --log-file -" > Procfile
   
   # Create runtime.txt
   echo "python-3.11.0" > runtime.txt
   
   # Update requirements.txt
   pip freeze > requirements.txt
   # Add these if not present:
   # gunicorn
   # psycopg2-binary
   # whitenoise
   # dj-database-url
   ```

3. **Update settings.py**
   ```python
   # Add to config/settings.py
   
   import dj_database_url
   
   # Database
   if 'DATABASE_URL' in os.environ:
       DATABASES['default'] = dj_database_url.config(
           conn_max_age=600,
           ssl_require=True
       )
   
   # Static files
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   
   # Middleware (add after SecurityMiddleware)
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
       # ... rest of middleware
   ]
   ```

4. **Deploy to Heroku**
   ```bash
   # Login
   heroku login
   
   # Create app
   heroku create uog-complaints-backend
   
   # Add PostgreSQL
   heroku addons:create heroku-postgresql:mini
   
   # Set environment variables
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="uog-complaints-backend.herokuapp.com"
   heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
   heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
   
   # Deploy
   git init
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   
   # Run migrations
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku run python manage.py seed_data
   ```

#### Frontend Deployment (Vercel)

1. **Update API URL**
   ```javascript
   // frontend/src/api.js
   const api = axios.create({
     baseURL: 'https://uog-complaints-backend.herokuapp.com/api/',
   });
   ```

2. **Deploy to Vercel**
   ```bash
   cd frontend
   
   # Install Vercel CLI
   npm i -g vercel
   
   # Login
   vercel login
   
   # Deploy
   vercel --prod
   ```

3. **Update CORS in Backend**
   ```python
   # backend/config/settings.py
   CORS_ALLOWED_ORIGINS = [
       'https://your-app.vercel.app',
   ]
   ```

### Option 2: AWS (Production Grade)

#### Backend on AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.small or larger
   - Security group: Allow 80, 443, 22

2. **SSH and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv nginx -y
   
   # Clone your repo
   git clone https://github.com/your-repo/complaint-system.git
   cd complaint-system/backend
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Configure Gunicorn**
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/gunicorn.service
   ```
   
   ```ini
   [Unit]
   Description=Gunicorn daemon for UoG Complaints
   After=network.target
   
   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/complaint-system/backend
   Environment="PATH=/home/ubuntu/complaint-system/backend/venv/bin"
   ExecStart=/home/ubuntu/complaint-system/backend/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/home/ubuntu/complaint-system/backend/gunicorn.sock \
             config.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Start service
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

4. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/complaints
   ```
   
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /home/ubuntu/complaint-system/backend;
       }
       
       location /media/ {
           root /home/ubuntu/complaint-system/backend;
       }
   
       location / {
           include proxy_params;
           proxy_pass http://unix:/home/ubuntu/complaint-system/backend/gunicorn.sock;
       }
   }
   ```
   
   ```bash
   # Enable site
   sudo ln -s /etc/nginx/sites-available/complaints /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

#### Frontend on AWS S3 + CloudFront

1. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Create S3 Bucket**
   - Name: uog-complaints-frontend
   - Enable static website hosting
   - Upload dist/ contents

3. **Create CloudFront Distribution**
   - Origin: S3 bucket
   - Enable HTTPS
   - Set default root object: index.html

### Option 3: DigitalOcean (Balanced)

#### Using App Platform

1. **Backend**
   - Connect GitHub repo
   - Select backend folder
   - Environment: Python
   - Add PostgreSQL database
   - Set environment variables

2. **Frontend**
   - Connect GitHub repo
   - Select frontend folder
   - Environment: Node.js
   - Build command: `npm run build`
   - Output directory: `dist`

## Database Migration

### From SQLite to PostgreSQL

1. **Dump SQLite Data**
   ```bash
   python manage.py dumpdata > data.json
   ```

2. **Configure PostgreSQL**
   ```python
   # settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'complaints_db',
           'USER': 'postgres',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Load Data**
   ```bash
   python manage.py migrate
   python manage.py loaddata data.json
   ```

## Email Configuration

### Using Gmail

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=UoG Complaints <your-email@gmail.com>
```

### Using SendGrid

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=UoG Complaints <noreply@yourdomain.com>
```

### Using AWS SES

```bash
pip install django-ses
```

```python
# settings.py
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
```

## Environment Variables

### Backend (.env)

```env
# Django
SECRET_KEY=your-very-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=UoG Complaints <noreply@yourdomain.com>

# Frontend URL (for emails)
FRONTEND_URL=https://your-frontend-domain.com

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Frontend (.env)

```env
VITE_API_URL=https://your-backend-domain.com/api/
```

## Security Hardening

### Django Settings

```python
# config/settings.py

# Security
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]
CORS_ALLOW_CREDENTIALS = True
```

### Nginx Security Headers

```nginx
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## Monitoring and Logging

### Sentry Integration

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/complaints/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## Backup Strategy

### Database Backups

```bash
# Automated daily backup
0 2 * * * pg_dump complaints_db > /backups/db_$(date +\%Y\%m\%d).sql
```

### Media Files Backup

```bash
# Sync to S3
aws s3 sync /path/to/media s3://your-bucket/media-backup/
```

## Performance Optimization

### Enable Caching

```bash
pip install django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Database Optimization

```python
# Use select_related and prefetch_related
complaints = Complaint.objects.select_related(
    'submitter', 'assigned_to', 'campus'
).prefetch_related('files', 'comments')
```

### Frontend Optimization

```bash
# Build with optimization
npm run build

# Analyze bundle size
npm install --save-dev vite-plugin-bundle-analyzer
```

## Post-Deployment

### 1. Test Everything
- [ ] User registration
- [ ] Login/logout
- [ ] Complaint submission
- [ ] File uploads
- [ ] Email notifications
- [ ] Search and filters
- [ ] Comments
- [ ] Status updates

### 2. Monitor
- [ ] Check error logs
- [ ] Monitor response times
- [ ] Track email delivery
- [ ] Watch database performance

### 3. Backup
- [ ] Verify automated backups
- [ ] Test restore procedure
- [ ] Document backup locations

### 4. Documentation
- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Create runbook for common issues

## Rollback Plan

If deployment fails:

1. **Revert Code**
   ```bash
   git revert HEAD
   git push heroku main
   ```

2. **Restore Database**
   ```bash
   heroku pg:backups:restore
   ```

3. **Check Logs**
   ```bash
   heroku logs --tail
   ```

## Maintenance

### Regular Tasks
- Weekly: Review error logs
- Monthly: Update dependencies
- Quarterly: Security audit
- Yearly: Performance review

### Updates
```bash
# Update dependencies
pip list --outdated
pip install --upgrade package-name

# Run tests
python manage.py test

# Deploy
git push heroku main
```

## Support Contacts

- **Hosting Issues**: Contact your hosting provider
- **Email Issues**: Check email service status
- **Database Issues**: Check database logs
- **Code Issues**: Review error logs and Sentry

## Success Metrics

Track these after deployment:
- Uptime: Target 99.9%
- Response time: < 500ms
- Error rate: < 0.1%
- Email delivery: > 99%
- User satisfaction: > 4/5

---

**Deployment Checklist Complete**: ☐
**Production URL**: _______________
**Deployed By**: _______________
**Date**: _______________
