# Quick Development Guide

## 🚀 Getting Started (5 minutes)

### 1. Setup Environment
```bash
# Clone/download project
cd mysite

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
```

### 3. Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## 🎯 Quick Tour

### Main Pages
- **Home**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Signup**: http://127.0.0.1:8000/accounts/signup/

### Learning Examples
- **Hello World**: http://127.0.0.1:8000/hello/
- **Data Types**: http://127.0.0.1:8000/data-types/
- **Database**: http://127.0.0.1:8000/database/
- **Dashboard**: http://127.0.0.1:8000/dashboard/ (after login)

## 🛠️ Development Commands

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Setup groups and permissions
python manage.py setup_groups

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Create new Django app
python manage.py startapp appname

# Collect static files (for production)
python manage.py collectstatic
```

## 📁 Project Structure Quick Reference

```
mysite/
├── myapp/              # Main application
│   ├── models.py      # Database models
│   ├── views.py       # View functions
│   ├── forms.py       # Django forms
│   └── admin.py       # Admin configuration
│
├── templates/         # HTML templates
│   ├── base.html     # Base template
│   ├── accounts/     # User-related templates
│   └── examples/     # Learning examples
│
├── static/           # CSS, JS, images
├── docs/            # Documentation & guides
├── examples/        # Database relationship examples
└── manage.py        # Django management script
```

## 🎓 Learning Resources

1. **Start Here**: `docs/Views_to_Templates_Guide.md`
2. **Code Examples**: `docs/complete_view_examples.py`
3. **URL Routing**: `docs/example_urls.py`
4. **Database Examples**: `examples/` directory

## 🔧 Common Tasks

### Add a New Page
1. Create view function in `myapp/views.py`
2. Create HTML template in `templates/`
3. Add URL pattern in `mysite/urls.py` or `myapp/urls.py`

### Add Database Model
1. Define model in `myapp/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Add to admin in `myapp/admin.py` (optional)

### Style Changes
1. Edit `templates/base.html` for global styles
2. Add CSS to `static/css/` directory
3. Use Bootstrap classes (already included)

## 🐛 Troubleshooting

**Server won't start**
- Check if virtual environment is activated
- Install requirements: `pip install -r requirements.txt`

**Database errors**
- Run migrations: `python manage.py migrate`
- Delete db.sqlite3 and re-run migrations if needed

**Permission errors**
- Run: `python manage.py setup_groups`
- Assign users to groups in admin panel

**Templates not found**
- Check template path matches view
- Verify template extends `base.html`

---

**Happy Coding!** 🚀
