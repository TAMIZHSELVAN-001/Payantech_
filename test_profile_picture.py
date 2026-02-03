#!/usr/bin/env python
"""
Test script to verify profile picture setup
Run with: python test_profile_picture.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payantech.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile
from django.conf import settings

print("=" * 60)
print("PROFILE PICTURE SETUP TEST")
print("=" * 60)

# Test 1: Check media folder exists
print("\n1. Checking media folder configuration...")
media_root = settings.MEDIA_ROOT
media_url = settings.MEDIA_URL
print(f"   MEDIA_ROOT: {media_root}")
print(f"   MEDIA_URL: {media_url}")

if os.path.exists(media_root):
    print(f"   ✓ Media folder exists")
else:
    print(f"   ✗ Media folder does NOT exist")
    print(f"   Creating folder: {media_root}")
    os.makedirs(media_root, exist_ok=True)

profile_pics_dir = os.path.join(media_root, 'profile_pics')
if os.path.exists(profile_pics_dir):
    print(f"   ✓ Profile pictures folder exists")
else:
    print(f"   ✗ Profile pictures folder does NOT exist")
    print(f"   Creating folder: {profile_pics_dir}")
    os.makedirs(profile_pics_dir, exist_ok=True)

# Test 2: Check if any users exist
print("\n2. Checking users in database...")
users = User.objects.all()
print(f"   Total users: {users.count()}")

if users.count() > 0:
    for user in users:
        print(f"\n   User: {user.username}")
        try:
            profile = user.profile
            print(f"   - Profile exists: Yes")
            print(f"   - Has profile picture: {bool(profile.profile_picture)}")
            if profile.profile_picture:
                print(f"   - Picture file: {profile.profile_picture.name}")
                print(f"   - Picture URL: {profile.profile_picture.url}")
                full_path = profile.profile_picture.path
                print(f"   - Full path: {full_path}")
                print(f"   - File exists: {os.path.exists(full_path)}")
                print(f"   - File size: {os.path.getsize(full_path) if os.path.exists(full_path) else 'N/A'} bytes")
        except UserProfile.DoesNotExist:
            print(f"   - Profile exists: No (creating one now)")
            profile = UserProfile.objects.create(user=user)
            print(f"   - Profile created: Yes")
else:
    print("   No users found in database")

# Test 3: Check DEBUG setting
print("\n3. Checking Django settings...")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

# Test 4: Check database connection
print("\n4. Testing database connection...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM main_userprofile")
        count = cursor.fetchone()[0]
        print(f"   ✓ Database connected")
        print(f"   Total UserProfile records: {count}")
except Exception as e:
    print(f"   ✗ Database error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nNEXT STEPS:")
print("1. Run: python manage.py runserver")
print("2. Visit: http://localhost:8000/")
print("3. Login or register")
print("4. Go to profile page")
print("5. Try uploading a profile picture")
print("=" * 60)
