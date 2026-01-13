#!/usr/bin/env python
"""Create .env file with Microsoft OAuth configuration"""
import os

# Get values from environment or use placeholders
client_id = os.environ.get('MICROSOFT_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')
client_secret = os.environ.get('MICROSOFT_CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')
tenant_id = os.environ.get('MICROSOFT_TENANT_ID', 'YOUR_TENANT_ID_HERE')

env_content = f"""# Microsoft OAuth Configuration
MICROSOFT_CLIENT_ID={client_id}
MICROSOFT_CLIENT_SECRET={client_secret}
MICROSOFT_TENANT_ID={tenant_id}
MICROSOFT_REDIRECT_URI=http://localhost:8000/api/auth/microsoft/callback

# OAuth Settings
OAUTH_ENABLED=True
OAUTH_PROVIDER_NAME=Microsoft
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print(".env file created successfully!")
