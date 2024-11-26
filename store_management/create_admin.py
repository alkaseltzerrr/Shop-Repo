import os
import django
from django.utils import timezone
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_management.settings')
django.setup()

from django.contrib.auth.models import User
from store_ops.models import Employee

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

try:
    # Create superuser if it doesn't exist
    if not User.objects.filter(username=username).exists():
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        # Create employee profile for superuser
        Employee.objects.create(
            user=superuser,
            phone='1234567890',
            role='MANAGER',
            active=True,
            hire_date=timezone.now(),
            salary=Decimal('5000.00')  # Default salary for admin
        )
        
        print(f"""
Superuser created successfully!
Username: {username}
Password: {password}
        """)
    else:
        print("Superuser already exists!")
except Exception as e:
    print(f"Error creating superuser: {str(e)}")
