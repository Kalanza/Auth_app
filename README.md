# Django User Management & Authentication System

A comprehensive Django web application demonstrating user management, authentication, permissions, and dynamic content rendering. This project serves as both a functional web application and an educational resource for learning Django development patterns.

## 🚀 Features

### User Management
- **Custom User Registration** with extended profiles
- **Login/Logout** functionality
- **Password Management** (change, reset)
- **User Profiles** with avatar upload and bio
- **Permission-based Access Control**

### Content Management
- **Article System** with CRUD operations
- **Author Management** and article relationships
- **Publishing Workflow** with draft/published states
- **Dynamic Content Rendering** based on user permissions

### Advanced Features
- **Group-based Permissions** (Members, Authors, Moderators, Admins)
- **Role-based Dashboard** with different views per user type
- **Search and Filtering** functionality
- **Responsive Design** with Bootstrap 5
- **Custom Management Commands** for setup

## 📁 Project Structure

```
mysite/
├── mysite/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py        # Main configuration
│   ├── urls.py           # Root URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
│
├── myapp/                 # Main Django application
│   ├── models.py         # User Profile & Article models
│   ├── views.py          # View functions and classes
│   ├── forms.py          # Custom forms
│   ├── admin.py          # Admin interface setup
│   ├── apps.py           # App configuration
│   ├── tests.py          # Unit tests
│   ├── migrations/       # Database migrations
│   └── management/       # Custom management commands
│       └── commands/
│           ├── setup_groups.py    # Creates user groups/permissions
│           └── demo_category_product.py  # Demo data creation
│
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── profile.html     # User profile page
│   ├── accounts/        # Authentication templates
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── user_list.html
│   │   └── admin_user_management.html
│   ├── registration/    # Auth forms
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── password_*.html
│   ├── examples/        # Tutorial templates
│   │   ├── hello_world.html
│   │   ├── data_types.html
│   │   └── database_example.html
│   └── errors/
│       └── 403.html
│
├── static/              # Static files (CSS, JS, images)
├── examples/            # Database relationship examples
├── docs/               # Documentation and guides
│   ├── Views_to_Templates_Guide.md
│   ├── complete_view_examples.py
│   └── example_urls.py
├── db.sqlite3          # SQLite database
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ installed
- Git (optional, for cloning)

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd mysite
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Setup Groups and Permissions
```bash
python manage.py setup_groups
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 👥 User Roles & Permissions

### Member (Default)
- Can create and edit their own articles
- Can view published articles
- Basic profile management

### Author  
- All Member permissions
- Can publish their own articles
- Enhanced article management

### Moderator
- All Author permissions
- Can edit any user's articles
- Can view all user profiles
- Content moderation capabilities

### Site Admin
- All permissions
- User management
- Group assignment
- System administration

## 🌟 Key Learning Examples

This project demonstrates essential Django patterns:

### 1. Views to Templates Data Flow
- **Location**: `docs/complete_view_examples.py`
- **Templates**: `templates/examples/`
- **Covers**: Context passing, template syntax, filters, loops

### 2. Database Relationships
- **Location**: `examples/` directory
- **Covers**: ForeignKey, OneToOne, ManyToMany relationships

### 3. Authentication & Permissions
- **Models**: Custom UserProfile extending Django User
- **Views**: Permission decorators and mixins
- **Templates**: Conditional rendering based on permissions

### 4. Form Handling
- **Custom Forms**: User registration, profile updates
- **Validation**: Server-side form validation
- **File Uploads**: Avatar image handling

## 🔧 Key Django Concepts Demonstrated

### Models & Database
```python
# Extended User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

# Content Model with Permissions
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        permissions = [
            ("can_publish_article", "Can publish articles"),
        ]
```

### Views & Templates
```python
# Function-based view with context
def dashboard_view(request):
    context = {
        'user_groups': request.user.groups.all(),
        'user_permissions': request.user.get_all_permissions(),
        'total_articles': Article.objects.count(),
    }
    return render(request, 'dashboard.html', context)

# Class-based view with permissions
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'myapp.can_view_all_profiles'
```

### Template Patterns
```html
<!-- Conditional rendering -->
{% if user.has_perm:'myapp.can_publish_article' %}
    <a href="{% url 'publish_article' %}" class="btn btn-primary">Publish</a>
{% endif %}

<!-- Loop through QuerySet -->
{% for article in articles %}
    <h3>{{ article.title }}</h3>
    <p>By {{ article.author.username }} on {{ article.created_at|date:"F d, Y" }}</p>
{% endfor %}
```

## 📚 Educational Resources

### Documentation Files
- **`docs/Views_to_Templates_Guide.md`** - Comprehensive guide on passing data from views to templates
- **`docs/complete_view_examples.py`** - 7 detailed view examples with explanations
- **`examples/`** - Database relationship patterns and best practices

### Tutorial URLs
Add these to your `urls.py` to access learning examples:
- `/hello/` - Basic data passing
- `/data-types/` - All data types and template patterns  
- `/database/` - Database queries and relationships
- `/dashboard/` - User-specific content

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📱 API Endpoints

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/signup/` - User registration
- `POST /accounts/logout/` - User logout

### User Management
- `GET /profile/` - View/edit user profile
- `GET /dashboard/` - User dashboard
- `GET /users/` - User list (permission required)

### Admin Functions
- `GET /admin/users/` - User management interface
- `POST /admin/users/` - Update user groups

## 🔒 Security Features

- **CSRF Protection** on all forms
- **Permission-based Access Control** 
- **User Input Validation** and sanitization
- **SQL Injection Prevention** through Django ORM
- **XSS Protection** with template escaping

## 🚀 Deployment Considerations

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
```

### Production Settings
- Change `DEBUG = False` in settings.py
- Configure proper database (PostgreSQL recommended)
- Set up static file serving (WhiteNoise or CDN)
- Configure email backend for password resets

## 🤝 Contributing

This project serves as an educational resource. Contributions welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

**Permission Denied (403)**
- Run `python manage.py setup_groups` to create user groups
- Ensure user is assigned to appropriate group

**Template Not Found**
- Check `TEMPLATES` setting in `settings.py`
- Verify template file path matches view

**Database Errors**
- Run `python manage.py makemigrations` 
- Run `python manage.py migrate`

**Static Files Not Loading**
- Run `python manage.py collectstatic` for production
- Check `STATIC_URL` and `STATIC_ROOT` settings

## 📧 Support

For questions or issues:
1. Check the documentation in `docs/`
2. Review the example code
3. Create an issue on the repository

---

**Happy Coding!** 🚀

This Django project demonstrates real-world patterns and best practices. Use it as a learning resource or starting point for your own Django applications.
