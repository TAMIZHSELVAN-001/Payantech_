#!/usr/bin/env python
"""
Test script to create a test user and upload a sample profile picture
Run with: python setup_test_user.py
"""

import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payantech.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile
from django.core.files.base import ContentFile

print("=" * 60)
print("TEST USER & PROFILE PICTURE SETUP")
print("=" * 60)

# Step 1: Create test user
print("\n1. Creating test user...")
test_username = "testuser"
test_email = "testuser@example.com"
test_password = "TestPass123"

try:
    user = User.objects.get(username=test_username)
    print(f"   User '{test_username}' already exists")
except User.DoesNotExist:
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password
    )
    print(f"   ✓ Created user: {test_username}")

# Step 2: Get or create profile
print("\n2. Getting or creating profile...")
try:
    profile = user.profile
    print(f"   ✓ Profile exists for {test_username}")
except UserProfile.DoesNotExist:
    profile = UserProfile.objects.create(user=user)
    print(f"   ✓ Created profile for {test_username}")

# Step 3: Create a test image
print("\n3. Creating test profile picture...")
try:
    # Create a colorful test image
    img = Image.new('RGB', (200, 200), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple circle
    draw.ellipse([20, 20, 180, 180], fill='#764ba2', outline='white', width=5)
    
    # Draw some text
    try:
        draw.text((60, 90), "TEST", fill='white')
    except:
        # Font loading might fail, that's ok
        pass
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    
    # Save to profile
    filename = f'{user.id}_test_profile.jpg'
    profile.profile_picture.save(filename, ContentFile(img_io.read()), save=True)
    
    print(f"   ✓ Profile picture created and saved")
    print(f"   - File: {profile.profile_picture.name}")
    print(f"   - URL: {profile.profile_picture.url}")
    print(f"   - Path: {profile.profile_picture.path}")
    
    # Verify file exists
    if os.path.exists(profile.profile_picture.path):
        file_size = os.path.getsize(profile.profile_picture.path)
        print(f"   - File size: {file_size} bytes")
        print(f"   - File exists: Yes ✓")
    else:
        print(f"   - File exists: No ✗")
        
except Exception as e:
    print(f"   ✗ Error creating image: {e}")

# Step 4: Display user info
print("\n4. User Information:")
print(f"   Username: {user.username}")
print(f"   Email: {user.email}")
print(f"   Password: {test_password}")
print(f"   Has profile picture: {bool(profile.profile_picture)}")

print("\n" + "=" * 60)
print("SETUP COMPLETE")
print("=" * 60)
print("\nTO TEST:")
print(f"1. Start server: python manage.py runserver")
print(f"2. Visit: http://localhost:8000/")
print(f"3. Login with:")
print(f"   Username: {test_username}")
print(f"   Password: {test_password}")
print(f"4. Click on 'Profile' in navbar")
print(f"5. You should see the test picture displayed")
print("=" * 60)
