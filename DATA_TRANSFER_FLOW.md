# Payantech - Data Transfer Flow Documentation

This document illustrates how data flows through the Payantech Django application.

---

## 1. LOGIN FLOW

### User Interaction → Data Transfer → Backend Processing

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER LOGIN FLOW                             │
└─────────────────────────────────────────────────────────────────┘

FRONTEND (HTML/JavaScript)
├── loginpage.html (Login Form)
│   ├── Input Fields:
│   │   ├── username (type: text, name: "username")
│   │   └── password (type: password, name: "password")
│   │
│   └── Form Submission:
│       ├── Method: POST
│       ├── Action: {% url 'login' %} → /
│       └── Security: {% csrf_token %}
│
├── login.js (Client-side Validation)
│   ├── Event: DOMContentLoaded
│   ├── Validation: Check username & password not empty
│   └── Notification: Shows success/error messages
│
└── login.css (UI Styling)
    └── Displays error/success notifications


BACKEND (Django)
├── views.py → login_view(request)
│   │
│   ├── REQUEST RECEIVED:
│   │   ├── Method: POST
│   │   ├── Data: 
│   │   │   ├── request.POST.get('username')
│   │   │   └── request.POST.get('password')
│   │   └── CSRF Token: Validated
│   │
│   ├── AUTHENTICATION:
│   │   └── authenticate(request, username=username, password=password)
│   │       └── Checks Django User model in database
│   │
│   ├── RESPONSE (Success):
│   │   ├── login(request, user) → Creates session
│   │   ├── messages.success() → "Login successful!"
│   │   └── Redirect to: home
│   │
│   └── RESPONSE (Failure):
│       ├── messages.error() → "Invalid username or password"
│       └── Render: loginpage.html


DATABASE (SQLite: db.sqlite3)
├── Django User Model
│   ├── username
│   ├── password (hashed)
│   ├── email
│   └── Other auth fields
│
└── User Session Created (on success)
    └── Stored in session storage


RESPONSE FLOW BACK TO FRONTEND
├── Server Response:
│   ├── If Success:
│   │   ├── Redirect response (HTTP 302)
│   │   ├── Session cookie set
│   │   └── Browser navigates to /home/
│   │
│   └── If Failure:
│       ├── HTML response with loginpage.html
│       ├── Django messages in template context
│       └── Messages appear in UI via login.js
│
└── Frontend Display:
    ├── Notification displays message
    ├── Auto-close after 5 seconds
    └── User sees feedback
```

---

## 2. REGISTRATION FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER REGISTRATION FLOW                        │
└─────────────────────────────────────────────────────────────────┘

FRONTEND
├── loginpage.html (Register Form - Hidden by default)
│   ├── Input Fields:
│   │   ├── username (type: text)
│   │   ├── email (type: email)
│   │   └── password (type: password)
│   │
│   └── Form Submission:
│       ├── Method: POST
│       ├── Action: {% url 'register' %} → /register/
│       └── Trigger: "Sign Up" link click


BACKEND
├── views.py → register_view(request)
│   │
│   ├── REQUEST DATA:
│   │   ├── username = request.POST.get('username')
│   │   ├── email = request.POST.get('email')
│   │   └── password = request.POST.get('password')
│   │
│   ├── VALIDATION:
│   │   ├── Check if User with username exists
│   │   │   └── User.objects.filter(username=username).exists()
│   │   │
│   │   ├── If Exists:
│   │   │   └── messages.error() → "Username already exists"
│   │   │
│   │   └── If Not Exists:
│   │       └── CREATE NEW USER:
│   │           ├── User.objects.create_user(
│   │           │   username=username,
│   │           │   email=email,
│   │           │   password=password
│   │           │)
│   │           ├── messages.success() → "Account created successfully"
│   │           └── Redirect to: login


DATABASE
├── New User Record Created:
│   ├── username (unique)
│   ├── email
│   ├── password (hashed by Django)
│   └── is_active = True (by default)
│
└── Associated UserProfile (Optional)
    ├── user (OneToOneField)
    ├── phone
    ├── bio
    ├── profile_picture
    ├── created_at
    └── updated_at


RESPONSE
├── Success: Redirect to /login/
│   └── User sees confirmation message
│
└── Failure: Render registration form with error
    └── User informed to use different username
```

---

## 3. HOME PAGE FLOW (Authenticated Users)

```
┌─────────────────────────────────────────────────────────────────┐
│                      HOME PAGE DATA FLOW                         │
└─────────────────────────────────────────────────────────────────┘

FRONTEND
└── index.html (Rendered with user data)


BACKEND
├── views.py → home(request)
│   │
│   ├── REQUEST:
│   │   └── GET request to /home/
│   │
│   ├── USER CHECK:
│   │   ├── request.user (Django middleware sets this)
│   │   └── request.user.is_authenticated (Boolean)
│   │
│   ├── CONTEXT PREPARATION:
│   │   ├── Prepare context dictionary:
│   │   │   ├── 'user': request.user (User object)
│   │   │   ├── 'username': request.user.username (if authenticated)
│   │   │   └── 'email': request.user.email (if authenticated)
│   │   │
│   │   └── Pass to template:
│   │       └── render(request, 'index.html', context)
│   │
│   └── RESPONSE:
│       └── Rendered HTML with user data injected


TEMPLATE (index.html)
├── Access passed context variables:
│   ├── {{ user }} → User object
│   ├── {{ username }} → Logged-in user's username
│   └── {{ email }} → Logged-in user's email
│
└── Display personalized content:
    ├── "Welcome, {{ username }}!"
    └── Show email if available


DATABASE
└── No new data written (read-only)
    └── Session validation via middleware
```

---

## 4. CONTACT FORM FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONTACT FORM DATA FLOW                         │
└─────────────────────────────────────────────────────────────────┘

FRONTEND
├── contact.html (Contact Form)
│   ├── Input Fields:
│   │   ├── <input name="name" type="text">
│   │   ├── <input name="email" type="email">
│   │   ├── <input name="phone" type="text">
│   │   └── <textarea name="message">
│   │
│   └── Form Submission:
│       ├── Method: POST
│       ├── Action: {% url 'contact' %} → /contact/
│       └── CSRF Token: {% csrf_token %}


BACKEND
├── views.py → contact(request)
│   │
│   ├── REQUEST HANDLING:
│   │   ├── Check if POST request
│   │   │
│   │   └── If POST:
│   │       ├── Extract form data:
│   │       │   ├── name = request.POST.get('name')
│   │       │   ├── email = request.POST.get('email')
│   │       │   ├── phone = request.POST.get('phone')
│   │       │   └── message = request.POST.get('message')
│   │       │
│   │       ├── CREATE DATABASE RECORD:
│   │       │   └── ContactMessage.objects.create(
│   │       │       name=name,
│   │       │       email=email,
│   │       │       phone=phone,
│   │       │       message=message
│   │       │   )
│   │       │
│   │       └── RESPONSE:
│   │           └── render(request, 'contact.html', 
│   │               {'success': True})
│   │
│   └── If GET: render(request, 'contact.html')


DATABASE
├── ContactMessage Table:
│   ├── id (auto-generated primary key)
│   ├── name (CharField, max_length=100)
│   ├── email (EmailField)
│   ├── phone (CharField, max_length=20)
│   ├── message (TextField)
│   └── submitted_at (DateTimeField, auto_now_add=True)
│
└── New Record Example:
    ├── id: 1
    ├── name: "John Doe"
    ├── email: "john@example.com"
    ├── phone: "+1234567890"
    ├── message: "I'm interested in your services..."
    └── submitted_at: 2026-01-27 10:30:45


TEMPLATE RESPONSE
└── contact.html re-renders with:
    ├── {% if success %}
    │   └── <p style="color:green;">Message sent successfully!</p>
    └── Form cleared for next submission
```

---

## 5. LOGOUT FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                      LOGOUT DATA FLOW                            │
└─────────────────────────────────────────────────────────────────┘

FRONTEND
└── Click logout link


BACKEND
├── views.py → logout_view(request)
│   │
│   ├── SESSION CLEANUP:
│   │   └── logout(request)
│   │       ├── Clears session data
│   │       └── Removes session cookie
│   │
│   └── RESPONSE:
│       └── Redirect to /login/


DATABASE
└── Session data deleted
    └── User no longer authenticated
```

---

## 6. DATA MODELS SUMMARY

### User Model (Built-in Django)
```
User (Django built-in)
├── username: unique CharField
├── email: EmailField
├── password: hashed CharField
├── is_active: Boolean
├── is_staff: Boolean
├── is_superuser: Boolean
├── first_name: CharField
├── last_name: CharField
└── date_joined: DateTimeField
```

### UserProfile Model (Extended User Data)
```
UserProfile
├── user: OneToOneField → User (CASCADE delete)
├── phone: CharField (optional)
├── bio: TextField (optional)
├── profile_picture: ImageField (optional)
├── created_at: DateTimeField (auto_now_add)
└── updated_at: DateTimeField (auto_now)
```

### ContactMessage Model
```
ContactMessage
├── id: AutoField (Primary Key)
├── name: CharField (max_length=100)
├── email: EmailField
├── phone: CharField (max_length=20)
├── message: TextField
└── submitted_at: DateTimeField (auto_now_add)
```

---

## 7. URL ROUTING MAP

```
URL Pattern          → View Function      → Template        → Purpose
─────────────────────────────────────────────────────────────────
/ (GET)              → login_view()       → loginpage.html   → Display login form
/ (POST)             → login_view()       → loginpage.html   → Process login
/register/ (POST)    → register_view()    → loginpage.html   → Process registration
/home/ (GET)         → home()             → index.html       → Home page
/services/ (GET)     → services()         → services.html    → Services page
/contact/ (GET)      → contact()          → contact.html     → Display contact form
/contact/ (POST)     → contact()          → contact.html     → Save contact message
/logout/ (GET)       → logout_view()      → [redirect]       → Clear session
```

---

## 8. SECURITY NOTES

```
Security Feature                Implementation
──────────────────────────────────────────────────────────
CSRF Protection              {% csrf_token %} in all forms
Password Hashing             Django User.objects.create_user()
Session Management          Django middleware (request.user)
SQL Injection Prevention     Django ORM (objects.create, get, filter)
Authentication              Django authenticate() + login()
User Validation             is_authenticated property
```

---

## 9. DATA FLOW DIAGRAM (ASCII Art)

```
                          ┌──────────────┐
                          │   Browser    │
                          │   (Frontend) │
                          └──────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
              HTML/CSS        JavaScript    Form Data
            (Rendering)    (Validation)   (POST/GET)
                    │            │            │
                    └────────────┼────────────┘
                                 │
                          ┌──────▼────────┐
                          │   URL Router  │
                          │  (urls.py)    │
                          └──────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
           /login/           /register/       /contact/
           /home/            /logout/         /services/
                │                │                │
                └────────────────┼────────────────┘
                                 │
                          ┌──────▼──────────┐
                          │   Django Views  │
                          │  (views.py)     │
                          └──────┬──────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
              Authenticate   Validate Form   Query Data
              Create User     Create Message  Render Template
                    │            │            │
                    └────────────┼────────────┘
                                 │
                          ┌──────▼────────────┐
                          │   Django ORM     │
                          │  (models.py)     │
                          └──────┬───────────┘
                                 │
                          ┌──────▼─────────┐
                          │  SQLite DB     │
                          │ (db.sqlite3)   │
                          │                │
                          │ • Users        │
                          │ • Sessions     │
                          │ • Contacts     │
                          │ • Messages     │
                          └────────────────┘
```

---

## 10. REQUEST/RESPONSE CYCLE EXAMPLE: LOGIN

```
Step 1: User enters credentials
├── Username: "john_doe"
└── Password: "password123"

Step 2: Browser sends POST request
├── URL: http://localhost:8000/
├── Method: POST
├── Headers:
│   ├── Content-Type: application/x-www-form-urlencoded
│   └── Cookie: csrftoken=xxxxx
└── Body: username=john_doe&password=password123&csrfmiddlewaretoken=xxxxx

Step 3: Django processes request
├── CSRF token validated ✓
├── Data extracted from request.POST
├── authenticate(request, username="john_doe", password="password123")
├── If user found in database:
│   ├── Passwords match (hashed comparison)
│   ├── login(request, user) called
│   └── Session created
└── Database query: SELECT * FROM auth_user WHERE username='john_doe'

Step 4: Response sent back
├── If Success:
│   ├── HTTP Response: 302 Redirect
│   ├── Location: /home/
│   ├── Set-Cookie: sessionid=xxxxx
│   └── Browser follows redirect to /home/
│
└── If Failure:
    ├── HTTP Response: 200 OK
    ├── HTML: loginpage.html rendered
    ├── Django Messages in context
    └── JavaScript displays error notification

Step 5: Frontend displays result
├── Notification appears
├── Auto-closes after 5 seconds
└── User sees feedback
```

---

## 11. Key Technologies & Their Roles

```
Technology          Role                          Data Handled
──────────────────────────────────────────────────────────────
HTML                Structure & Form fields       Form inputs
CSS                 Styling & Layout              UI presentation
JavaScript          Client-side validation        User input validation
Django Views        Business logic                Form processing
Django Models       Data structure definition     Data schema
Django ORM          Database abstraction          SQL queries
SQLite              Persistent data storage       All application data
Django Templates    Server-side rendering        Dynamic HTML generation
Sessions            User state management        Logged-in user data
CSRF Tokens         Security                     XSS prevention
```

---

## Summary

Your Payantech application follows a classic **Django MTV (Model-Template-View)** architecture:

1. **Models** define what data looks like (User, UserProfile, ContactMessage)
2. **Templates** define how data is displayed (HTML with Django template tags)
3. **Views** process requests, interact with models, and pass data to templates
4. **Forms** collect data from users (HTML forms with CSRF protection)
5. **Database** persistently stores data (SQLite)

Data flows in a cycle:
- **Browser** → **Form submission (POST/GET)**
- **Django Router** → **Matches URL pattern**
- **Django View** → **Processes request, accesses database**
- **Database** → **Stores/retrieves data**
- **View** → **Prepares response**
- **Template** → **Renders HTML with data**
- **Browser** → **Displays to user**
