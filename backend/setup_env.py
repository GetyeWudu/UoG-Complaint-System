#!/usr/bin/env python
"""Setup .env file with all required configuration"""
import os

# Check if .env exists
env_path = '.env'
env_exists = os.path.exists(env_path)

# Read existing .env if it exists
existing_vars = {}
if env_exists:
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                existing_vars[key.strip()] = value.strip()

# Microsoft OAuth Configuration (required)
# Get from environment variables or use placeholders
required_vars = {
    'MICROSOFT_CLIENT_ID': os.environ.get('MICROSOFT_CLIENT_ID', existing_vars.get('MICROSOFT_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')),
    'MICROSOFT_CLIENT_SECRET': os.environ.get('MICROSOFT_CLIENT_SECRET', existing_vars.get('MICROSOFT_CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')),
    'MICROSOFT_TENANT_ID': os.environ.get('MICROSOFT_TENANT_ID', existing_vars.get('MICROSOFT_TENANT_ID', 'YOUR_TENANT_ID_HERE')),
    'MICROSOFT_REDIRECT_URI': 'http://localhost:8000/api/auth/microsoft/callback',
    'OAUTH_ENABLED': 'True',
    'OAUTH_PROVIDER_NAME': 'Microsoft',
    'FRONTEND_URL': 'http://localhost:5173',
}

# Optional variables with defaults
optional_vars = {
    'SECRET_KEY': existing_vars.get('SECRET_KEY', 'django-insecure-h-g$=*@umhw=z@^3!gd3tl*bg9jwnc2af0j*31!gdk9fd7siu*'),
    'DEBUG': existing_vars.get('DEBUG', 'True'),
    'ALLOWED_HOSTS': existing_vars.get('ALLOWED_HOSTS', '*'),
    'CSRF_TRUSTED_ORIGINS': existing_vars.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173'),
    'GROQ_API_KEY': existing_vars.get('GROQ_API_KEY', ''),
    'GROQ_CHATBOT_API_KEY': existing_vars.get('GROQ_CHATBOT_API_KEY', ''),
    'GEMINI_API_KEY': existing_vars.get('GEMINI_API_KEY', ''),
    'EMAIL_BACKEND': existing_vars.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'),
}

# Merge all variables
all_vars = {**required_vars, **optional_vars}

# Write .env file
with open(env_path, 'w', encoding='utf-8') as f:
    f.write('# Django Settings\n')
    f.write(f'SECRET_KEY={all_vars["SECRET_KEY"]}\n')
    f.write(f'DEBUG={all_vars["DEBUG"]}\n')
    f.write(f'ALLOWED_HOSTS={all_vars["ALLOWED_HOSTS"]}\n')
    f.write('\n')
    f.write('# Microsoft OAuth Configuration\n')
    f.write(f'MICROSOFT_CLIENT_ID={all_vars["MICROSOFT_CLIENT_ID"]}\n')
    f.write(f'MICROSOFT_CLIENT_SECRET={all_vars["MICROSOFT_CLIENT_SECRET"]}\n')
    f.write(f'MICROSOFT_TENANT_ID={all_vars["MICROSOFT_TENANT_ID"]}\n')
    f.write(f'MICROSOFT_REDIRECT_URI={all_vars["MICROSOFT_REDIRECT_URI"]}\n')
    f.write('\n')
    f.write('# OAuth Settings\n')
    f.write(f'OAUTH_ENABLED={all_vars["OAUTH_ENABLED"]}\n')
    f.write(f'OAUTH_PROVIDER_NAME={all_vars["OAUTH_PROVIDER_NAME"]}\n')
    f.write('\n')
    f.write('# Frontend URL\n')
    f.write(f'FRONTEND_URL={all_vars["FRONTEND_URL"]}\n')
    f.write('\n')
    f.write('# CSRF Trusted Origins\n')
    f.write(f'CSRF_TRUSTED_ORIGINS={all_vars["CSRF_TRUSTED_ORIGINS"]}\n')
    f.write('\n')
    f.write('# AI API Keys (Optional - leave empty if not using AI features)\n')
    f.write(f'GROQ_API_KEY={all_vars["GROQ_API_KEY"]}\n')
    f.write(f'GROQ_CHATBOT_API_KEY={all_vars["GROQ_CHATBOT_API_KEY"]}\n')
    f.write(f'GEMINI_API_KEY={all_vars["GEMINI_API_KEY"]}\n')
    f.write('\n')
    f.write('# Email Configuration (Optional)\n')
    f.write(f'EMAIL_BACKEND={all_vars["EMAIL_BACKEND"]}\n')

print(f".env file {'updated' if env_exists else 'created'} successfully!")
print("\nMicrosoft OAuth configuration:")
print(f"  Client ID: {all_vars['MICROSOFT_CLIENT_ID'][:20]}...")
print(f"  Tenant ID: {all_vars['MICROSOFT_TENANT_ID']}")
print(f"  Redirect URI: {all_vars['MICROSOFT_REDIRECT_URI']}")
print(f"  OAuth Enabled: {all_vars['OAUTH_ENABLED']}")
