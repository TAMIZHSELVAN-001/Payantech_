# Profile Picture Upload - Troubleshooting & Fix Guide

## Issues Fixed

### 1. **File Input not properly integrated with form**
   - **Problem**: The hidden file input wasn't part of the form element
   - **Solution**: Added `name="profile_picture"` to the file input and made sure it's positioned correctly in the DOM

### 2. **FormData not being sent properly**
   - **Problem**: JavaScript was trying to manually set FormData instead of letting the native form submission handle it
   - **Solution**: Removed manual FormData handling and let the form submit naturally with the file input

### 3. **Database Configuration Issue**
   - **Problem**: Settings were configured for PostgreSQL but SQLite was needed
   - **Solution**: Updated `.env` file to use SQLite with proper configuration

### 4. **Missing Signal Handlers**
   - **Problem**: UserProfile wasn't being created automatically when a User was created
   - **Solution**: Added Django signals in `signals.py` to auto-create UserProfile on User creation

### 5. **File Size and Type Validation**
   - **Problem**: No validation on client side before upload
   - **Solution**: Added JavaScript validation for file size (max 5MB) and type (image only)

---

## How Profile Picture Upload Now Works

### Step-by-Step Flow:

1. **User clicks "Upload Picture"**
   - JavaScript triggers file input dialog
   - User selects an image file

2. **File Validation**
   - Check file size ≤ 5MB
   - Check file type (JPEG, PNG, GIF, WebP)
   - Show preview of selected image
   - Display upload form

3. **User clicks "Upload Picture" in form**
   - Form submits as `multipart/form-data` (required for files)
   - Backend receives the file in `request.FILES['profile_picture']`

4. **Backend Processing (Django View)**
   - Delete old image file if exists
   - Save new image to `/media/profile_pics/`
   - Update UserProfile in database
   - Redirect back to profile page
   - Show success message

5. **Image Display**
   - Profile picture shows in circular container
   - "Remove Picture" button appears only if image exists

---

## Updated Key Components

### 1. File Structure Changes
```
main/
├── apps.py (NEW) - App configuration with signals
├── signals.py (NEW) - Auto-create UserProfile
├── models.py - Updated UserProfile model
├── views.py - Updated profile_view with image handling
├── templates/profile.html - Updated form and JavaScript
└── static/...
```

### 2. Database Configuration
**File: `.env`**
```
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**File: `settings.py`**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**File: `urls.py` (Main)**
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. HTML Form Setup
```html
<input type="file" id="profilePictureInput" name="profile_picture" accept="image/*">
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <!-- form content -->
</form>
```

### 4. JavaScript Fixes
- File validation before upload
- Proper form submission
- Drag-and-drop support with DataTransfer
- Preview image display
- Error handling

---

## Testing the Upload Feature

### Step 1: Start the Django Server
```bash
cd path/to/project
source .venv/Scripts/activate  # On Windows
python manage.py runserver
```

### Step 2: Login or Create Account
- Go to `http://localhost:8000/`
- Create a new account or login

### Step 3: Navigate to Profile
- Click "Profile" link in navbar
- Should see profile page

### Step 4: Upload Picture
- Click "Upload Picture" button
- Select an image file (JPG, PNG, GIF, WebP)
- Image preview should appear
- Click "Upload Picture" in the form
- Should see success message
- Profile picture should display

### Step 5: Remove Picture
- Click "Remove Picture" button
- Confirm deletion
- Picture should be removed
- Button should disappear

---

## File Size Limits

Current configuration:
- **Max file size**: 5 MB
- **Allowed formats**: JPEG, PNG, GIF, WebP

To change limits, edit in `profile.html` JavaScript:
```javascript
const maxSize = 5 * 1024 * 1024; // Change this value
const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']; // Add/remove types
```

---

## Directory Structure

```
project/
├── media/
│   └── profile_pics/
│       └── {user_id}_*.{ext}  ← Profile pictures stored here
├── .env  ← Database config
├── db.sqlite3  ← SQLite database
└── ...
```

---

## Common Issues & Solutions

### Issue: "No file chosen" or file not uploading
**Solution**: 
- Check file input has `name="profile_picture"`
- Ensure form has `enctype="multipart/form-data"`
- Check browser console for JavaScript errors

### Issue: "File size exceeded" error
**Solution**:
- Reduce image dimensions before uploading
- Convert to WebP format (smaller file size)
- Increase max file size in settings (if needed)

### Issue: "Invalid file type" error
**Solution**:
- Upload a valid image (JPEG, PNG, GIF, WebP)
- Check file extension matches actual file type

### Issue: Media files not displaying
**Solution**:
- Ensure `settings.DEBUG = True`
- Check media files path is correct
- Verify media URL configuration in Django settings

### Issue: "Profile picture does not uploaded" message
**Solution**:
- Check Django terminal for error messages
- Verify `/media/` folder has write permissions
- Clear browser cache and try again
- Check file format is valid

---

## Advanced Configuration (Optional)

### Compress images on upload
```python
# Install: pip install pillow-simd
from PIL import Image
import io

def compress_image(image_file, quality=85):
    img = Image.open(image_file)
    img = img.convert('RGB')
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=quality)
    img_io.seek(0)
    return img_io
```

### Store images in cloud (AWS S3)
- Install: `pip install boto3 django-storages`
- Configure S3 credentials in settings
- Images will be stored on S3 instead of local storage

---

## Summary of Changes Made

✅ Fixed file input integration with form  
✅ Removed faulty FormData manipulation  
✅ Changed database to SQLite  
✅ Added Django signals for auto UserProfile creation  
✅ Added file validation (size & type)  
✅ Fixed drag-drop functionality  
✅ Updated HTML form structure  
✅ Enhanced error handling  
✅ Added success messages  
✅ Configured media file serving  

The profile picture upload feature is now fully functional!
