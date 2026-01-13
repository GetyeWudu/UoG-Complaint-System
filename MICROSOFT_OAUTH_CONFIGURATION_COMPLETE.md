# Microsoft OAuth Configuration - Complete

## ✅ What Has Been Configured

### 1. Backend Code Updates
- ✅ Added `microsoft_login` and `microsoft_register` action types to ActivityLog model
- ✅ Updated `MicrosoftOAuthCallbackView` to handle both GET (redirect from Microsoft) and POST (from frontend) requests
- ✅ Added shared callback processing logic for both request types
- ✅ Updated frontend callback handler to support token-based authentication from backend redirect

### 2. Frontend Updates
- ✅ Updated `MicrosoftCallback.jsx` to handle tokens from URL query parameters (when redirected from backend)
- ✅ Maintains backward compatibility with code-based flow

### 3. Environment Configuration
The `.env` file needs to be created manually in the `backend` directory with the following content:

```env
# Microsoft OAuth Configuration
MICROSOFT_CLIENT_ID=YOUR_CLIENT_ID_HERE
MICROSOFT_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
MICROSOFT_TENANT_ID=YOUR_TENANT_ID_HERE
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback

# OAuth Settings
OAUTH_ENABLED=True
OAUTH_PROVIDER_NAME=Microsoft
```

**Important**: Replace the placeholder values with your actual Microsoft OAuth credentials from Azure Portal.

## 📋 Manual Steps Required

### Step 1: Create .env File
Create a file named `.env` in the `backend` directory with the content shown above.

You can use the provided script:
```bash
cd backend
python create_env.py
```

Or create it manually using any text editor.

### Step 2: Run Database Migrations
After creating the `.env` file, activate your virtual environment and run:

```bash
cd backend
# Activate your virtual environment first (if not already activated)
# On Windows: venv\Scripts\activate
# On Linux/Mac: source venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

### Step 3: Restart Backend Server
After creating the `.env` file, restart your Django backend server so it picks up the new environment variables:

```bash
cd backend
python manage.py runserver
```

### Step 4: Test the Integration
1. Start your frontend server: `npm run dev` (in the frontend directory)
2. Navigate to the login page
3. Click "Sign in with Microsoft"
4. You should be redirected to Microsoft's login page
5. After authentication, you'll be redirected back and logged in

## 🔄 How It Works

### Flow 1: Direct Backend Redirect (Current Setup)
1. User clicks "Sign in with Microsoft" on frontend
2. Frontend calls `GET /api/auth/microsoft/login/` to get authorization URL
3. User is redirected to Microsoft login page
4. Microsoft redirects to backend: `http://localhost:8000/api/auth/microsoft/callback?code=...&state=...`
5. Backend processes OAuth, creates/updates user, generates token
6. Backend redirects to frontend: `http://localhost:5173/auth/microsoft/callback?token=...&success=true`
7. Frontend extracts token, gets user data, and logs user in

### Flow 2: Frontend Code Exchange (Alternative)
1. User clicks "Sign in with Microsoft"
2. Frontend gets authorization URL from backend
3. User authenticates with Microsoft
4. Microsoft redirects to frontend with code and state
5. Frontend sends code and state to backend via POST
6. Backend processes and returns token
7. Frontend stores token and logs user in

## 🔍 Verification

To verify your configuration is correct, you can use Django shell:

```bash
cd backend
python manage.py shell
```

Then run:
```python
from accounts.microsoft_oauth import microsoft_oauth_service
print(f"Configured: {microsoft_oauth_service.is_configured()}")
print(f"Client ID: {microsoft_oauth_service.client_id[:10]}...")
print(f"Tenant ID: {microsoft_oauth_service.tenant_id}")
print(f"Redirect URI: {microsoft_oauth_service.redirect_uri}")
```

If `is_configured()` returns `True`, your configuration is correct!

## ⚠️ Important Notes

1. **Redirect URI**: Must match exactly what's configured in Azure Portal
   - Current: `http://localhost:8000/api/auth/microsoft/callback`
   - Make sure this is also set in your Azure AD app registration

2. **Environment Variables**: The backend server must be restarted after creating/updating the `.env` file

3. **Database Migrations**: The new ActivityLog action types require a migration

4. **Frontend URL**: The backend redirects to `http://localhost:5173/auth/microsoft/callback` by default. If your frontend runs on a different port, update `FRONTEND_URL` in your `.env` file.

## 🐛 Troubleshooting

### "Microsoft OAuth is not configured" error
- Check that `.env` file exists in `backend` directory
- Verify all environment variables are set correctly
- Restart the backend server

### "Invalid redirect URI" error
- Ensure redirect URI in Azure Portal matches `MICROSOFT_REDIRECT_URI` exactly
- Check for trailing slashes and protocol (http vs https)

### "Invalid state parameter" error
- Clear browser sessionStorage and try again
- Ensure cookies are enabled

## 📝 Files Modified

- `backend/accounts/models.py` - Added Microsoft OAuth action types
- `backend/accounts/views.py` - Updated callback view to handle GET requests
- `frontend/src/pages/MicrosoftCallback.jsx` - Added token-based authentication support
- `backend/create_env.py` - Helper script to create .env file (optional)

## ✨ Next Steps

1. Create the `.env` file (see Step 1 above)
2. Run migrations (see Step 2 above)
3. Restart backend server
4. Test the login flow
5. Enjoy Microsoft OAuth integration! 🎉
