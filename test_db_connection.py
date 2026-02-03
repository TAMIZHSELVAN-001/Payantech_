import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payantech.settings')
django.setup()

# Test the database connection
from django.db import connection
from django.db.utils import OperationalError

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✓ Database connection successful!")
    print(f"✓ Connected to: {connection.settings_dict['HOST']}:{connection.settings_dict['PORT']}")
    print(f"✓ Database: {connection.settings_dict['NAME']}")
    print(f"✓ Engine: {connection.settings_dict['ENGINE']}")
except OperationalError as e:
    print(f"✗ Database connection failed: {e}")
    sys.exit(1)
