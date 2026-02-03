from django.shortcuts import render, redirect
from .models import ContactMessage, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from PIL import Image
import os
import base64
import uuid
from django.core.files.base import ContentFile


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'loginpage.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, 'loginpage.html')


def logout_view(request):
    logout(request)
    return redirect('login')
    
def home(request):
    context = {
        'user': request.user,
        'username': request.user.username if request.user.is_authenticated else None,
        'email': request.user.email if request.user.is_authenticated else None,
    }
    return render(request, 'index.html', context)

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')


@login_required(login_url='login')
def update_profile_picture(user_profile, image_file):
    """
    Update user profile picture with validation and old image cleanup.
    
    Args:
        user_profile: UserProfile instance
        image_file: Uploaded image file
        
    Returns:
        dict: Status and message
    """
    try:
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if image_file.size > max_size:
            return {
                'success': False,
                'message': 'File size must be less than 5MB'
            }
        
        # Validate file type
        valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if image_file.content_type not in valid_types:
            return {
                'success': False,
                'message': 'Please upload a valid image file (JPEG, PNG, GIF, or WebP)'
            }
        
        # Validate image dimensions (optional)
        try:
            img = Image.open(image_file)
            # Reset file pointer after PIL reads it
            image_file.seek(0)
            min_width, min_height = 100, 100
            if img.width < min_width or img.height < min_height:
                return {
                    'success': False,
                    'message': f'Image must be at least {min_width}x{min_height} pixels'
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Invalid image file'
            }
        
        # Delete old image if exists
        if user_profile.profile_picture:
            old_image_path = user_profile.profile_picture.path
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception as e:
                    print(f"Error deleting old image: {e}")
        
        # Save new image
        user_profile.profile_picture = image_file
        user_profile.save()
        
        return {
            'success': True,
            'message': 'Profile picture updated successfully!'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error updating profile picture: {str(e)}'
        }


@login_required(login_url='login')
def remove_profile_picture(user_profile):
    """
    Remove user profile picture and delete the file.
    
    Args:
        user_profile: UserProfile instance
        
    Returns:
        dict: Status and message
    """
    try:
        if user_profile.profile_picture:
            # Get the file path before clearing the field
            image_path = user_profile.profile_picture.path
            
            # Delete from database
            user_profile.profile_picture = None
            user_profile.save()
            
            # Delete physical file
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"Error deleting image file: {e}")
            
            return {
                'success': True,
                'message': 'Profile picture removed successfully!'
            }
        else:
            return {
                'success': False,
                'message': 'No profile picture to remove'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error removing profile picture: {str(e)}'
        }


@login_required(login_url='login')
@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":

        # 🔍 DEBUG HERE
        print(request.FILES)
        print(request.POST)

        # ✅ normal upload (no crop)
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, "Profile picture updated")

        # ✅ cropped image (Base64)
        elif request.POST.get("cropped_image"):
            format, imgstr = request.POST["cropped_image"].split(";base64,")
            ext = format.split("/")[-1]

            file_name = f"profile_{uuid.uuid4()}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            profile.profile_picture = image_file
            profile.save()
            messages.success(request, "Profile picture updated")

        elif request.POST.get('delete_picture'):
            profile.profile_picture.delete(save=True)
            messages.success(request, "Profile picture removed")

    return render(request, "profile.html", {"profile": profile})





