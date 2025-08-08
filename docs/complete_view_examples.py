# =============================================================================
# DJANGO VIEWS TO TEMPLATES: Complete Beginner's Guide
# =============================================================================
# This file demonstrates how to pass data from Django views to templates
# and render dynamic content. Every part is explained for junior developers.
# =============================================================================

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Article, UserProfile

# =============================================================================
# EXAMPLE 1: BASIC VIEW - Passing Simple Data
# =============================================================================

def hello_world_view(request):
    """
    The simplest possible view that passes data to a template.
    
    WHAT THIS DOES:
    1. Defines a function that takes a 'request' parameter
    2. Creates a dictionary with data we want to send to the template
    3. Uses render() to combine the template with our data
    4. Returns the result as an HTTP response
    """
    # Step 1: Create a dictionary with data we want to pass to the template
    # This is called the "context" - it's the data bridge between views and templates
    context = {
        'greeting': 'Hello, World!',
        'current_time': datetime.now(),
        'app_name': 'My Django App',
        'version': '1.0.0'
    }
    
    # Step 2: Use render() to combine template with data
    # render() takes 3 parameters:
    # - request: the HTTP request object (always first parameter)
    # - template_name: path to the HTML template file
    # - context: dictionary with data to pass to template (optional)
    return render(request, 'examples/hello_world.html', context)

# =============================================================================
# EXAMPLE 2: PASSING DIFFERENT DATA TYPES
# =============================================================================

def data_types_example_view(request):
    """
    Shows how to pass different types of data to templates:
    strings, numbers, lists, dictionaries, booleans, etc.
    
    IMPORTANT: Templates can only display data, they can't execute complex Python code.
    So we prepare all the data here in the view before sending it to the template.
    """
    
    # String data
    user_name = "John Doe"
    welcome_message = "Welcome to our awesome website!"
    
    # Number data
    total_users = 1250
    average_age = 28.5
    
    # Boolean data
    is_premium_user = True
    has_notifications = False
    
    # List data (will be iterated in template using {% for %} loop)
    favorite_colors = ['Blue', 'Green', 'Purple', 'Orange']
    recent_activities = [
        'Logged in at 9:00 AM',
        'Updated profile picture',
        'Posted a new article',
        'Liked 3 posts'
    ]
    
    # Dictionary data (accessed in template using dot notation)
    user_stats = {
        'posts_count': 45,
        'followers': 1200,
        'following': 350,
        'likes_received': 2890
    }
    
    # List of dictionaries (common pattern for displaying multiple records)
    recent_posts = [
        {
            'title': 'Getting Started with Django',
            'date': '2025-01-15',
            'views': 250,
            'likes': 18
        },
        {
            'title': 'Understanding Django Templates',
            'date': '2025-01-10',
            'views': 180,
            'likes': 12
        },
        {
            'title': 'Building Your First Web App',
            'date': '2025-01-05',
            'views': 320,
            'likes': 25
        }
    ]
    
    # Pack everything into the context dictionary
    context = {
        # Basic data
        'user_name': user_name,
        'welcome_message': welcome_message,
        'total_users': total_users,
        'average_age': average_age,
        
        # Boolean flags (useful for conditional rendering)
        'is_premium_user': is_premium_user,
        'has_notifications': has_notifications,
        
        # Lists (for loops in templates)
        'favorite_colors': favorite_colors,
        'recent_activities': recent_activities,
        
        # Dictionary (dot notation access in templates)
        'user_stats': user_stats,
        
        # Complex data structures
        'recent_posts': recent_posts,
        
        # Computed values (calculations done here, not in template)
        'total_engagement': user_stats['posts_count'] + user_stats['likes_received'],
        'is_popular_user': user_stats['followers'] > 1000,
        
        # Page metadata
        'page_title': 'Data Types Demo',
        'page_description': 'Learn how different data types work in Django templates'
    }
    
    return render(request, 'examples/data_types.html', context)

# =============================================================================
# EXAMPLE 3: WORKING WITH DATABASE DATA
# =============================================================================

def database_example_view(request):
    """
    Shows how to fetch data from the database and pass it to templates.
    This is what you'll do most often in real Django applications.
    
    KEY CONCEPTS:
    - QuerySets: These are like database queries that return multiple records
    - Model instances: Single records from the database
    - select_related(): Optimizes database queries by joining related tables
    """
    
    # Fetch all articles from database
    # This creates a QuerySet - think of it as a list of Article objects
    all_articles = Article.objects.all()
    
    # Fetch only published articles (filtering)
    published_articles = Article.objects.filter(is_published=True)
    
    # Fetch articles with their authors (optimization - prevents extra database queries)
    articles_with_authors = Article.objects.select_related('author').filter(is_published=True)
    
    # Count total articles (more efficient than len(all_articles))
    total_articles_count = Article.objects.count()
    
    # Get the most recent article
    latest_article = Article.objects.filter(is_published=True).order_by('-created_at').first()
    
    # Fetch all users who have written articles
    authors = User.objects.filter(article__isnull=False).distinct()
    
    # Create summary statistics
    stats = {
        'total_articles': total_articles_count,
        'published_articles': published_articles.count(),
        'draft_articles': Article.objects.filter(is_published=False).count(),
        'total_authors': authors.count()
    }
    
    # Prepare context with all our database data
    context = {
        # QuerySets (lists of objects)
        'all_articles': all_articles,
        'published_articles': articles_with_authors,
        'authors': authors,
        
        # Single objects
        'latest_article': latest_article,
        
        # Statistics
        'stats': stats,
        
        # Page info
        'page_title': 'Articles from Database',
        'page_description': 'Displaying dynamic content from the database'
    }
    
    return render(request, 'examples/database_example.html', context)

# =============================================================================
# EXAMPLE 4: USER-SPECIFIC DATA (LOGIN REQUIRED)
# =============================================================================

@login_required  # This decorator ensures only logged-in users can access this view
def user_dashboard_view(request):
    """
    Shows how to create personalized views that display different content
    for each logged-in user. This is common for dashboards, profiles, etc.
    
    THE request OBJECT:
    - request.user: the currently logged-in user
    - request.method: 'GET', 'POST', etc.
    - request.GET: URL parameters (?param=value)
    - request.POST: form data
    """
    
    # Get the current user (this is automatically provided by Django)
    current_user = request.user
    
    # Get or create the user's profile
    try:
        user_profile = current_user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=current_user)
    
    # Get articles written by this user
    user_articles = Article.objects.filter(author=current_user).order_by('-created_at')
    
    # Calculate user statistics
    user_stats = {
        'total_articles': user_articles.count(),
        'published_articles': user_articles.filter(is_published=True).count(),
        'draft_articles': user_articles.filter(is_published=False).count(),
        'member_since': current_user.date_joined.strftime('%B %Y'),
        'last_login': current_user.last_login
    }
    
    # Get recent activity (last 5 articles)
    recent_articles = user_articles[:5]
    
    # Check user permissions (for conditional display in template)
    user_permissions = {
        'can_publish': current_user.has_perm('myapp.can_publish_article'),
        'can_view_all_profiles': current_user.has_perm('myapp.can_view_all_profiles'),
        'is_staff': current_user.is_staff,
        'is_superuser': current_user.is_superuser
    }
    
    context = {
        # User-specific data
        'current_user': current_user,
        'user_profile': user_profile,
        'user_articles': user_articles,
        'recent_articles': recent_articles,
        'user_stats': user_stats,
        'user_permissions': user_permissions,
        
        # Groups the user belongs to
        'user_groups': current_user.groups.all(),
        
        # Page info
        'page_title': f'Dashboard - {current_user.username}',
        'welcome_message': f'Welcome back, {current_user.first_name or current_user.username}!'
    }
    
    return render(request, 'examples/user_dashboard.html', context)

# =============================================================================
# EXAMPLE 5: DYNAMIC CONTENT BASED ON URL PARAMETERS
# =============================================================================

def article_detail_view(request, article_id):
    """
    Shows how to use URL parameters to display different content.
    The article_id comes from the URL pattern, like /article/123/
    
    URL PATTERNS:
    In urls.py, you'd have something like:
    path('article/<int:article_id>/', views.article_detail_view, name='article_detail')
    
    The <int:article_id> part captures the number from the URL and passes it
    to this function as the article_id parameter.
    """
    
    # Get the specific article or show 404 error if not found
    # get_object_or_404 is a Django shortcut that either:
    # - Returns the object if found
    # - Raises Http404 (shows 404 page) if not found
    article = get_object_or_404(Article, id=article_id, is_published=True)
    
    # Get the author's profile
    try:
        author_profile = article.author.userprofile
    except UserProfile.DoesNotExist:
        author_profile = None
    
    # Get other articles by the same author (excluding current article)
    other_articles = Article.objects.filter(
        author=article.author,
        is_published=True
    ).exclude(id=article.id).order_by('-created_at')[:3]
    
    # Get recent articles from all authors
    recent_articles = Article.objects.filter(
        is_published=True
    ).exclude(id=article.id).order_by('-created_at')[:5]
    
    # Determine if current user can edit this article
    can_edit_article = False
    if request.user.is_authenticated:
        can_edit_article = (
            request.user == article.author or 
            request.user.has_perm('myapp.change_article') or
            request.user.is_superuser
        )
    
    context = {
        # Main content
        'article': article,
        'author_profile': author_profile,
        
        # Related content
        'other_articles': other_articles,
        'recent_articles': recent_articles,
        
        # User permissions
        'can_edit_article': can_edit_article,
        'user_is_author': request.user == article.author if request.user.is_authenticated else False,
        
        # Page metadata
        'page_title': article.title,
        'page_description': article.content[:150] + '...' if len(article.content) > 150 else article.content
    }
    
    return render(request, 'examples/article_detail.html', context)

# =============================================================================
# EXAMPLE 6: HANDLING FORMS AND POST DATA
# =============================================================================

def contact_form_view(request):
    """
    Shows how to handle both GET and POST requests in the same view.
    This is common for forms that display on GET and process data on POST.
    
    HTTP METHODS:
    - GET: Used for displaying pages (like when you click a link)
    - POST: Used for submitting forms with data
    """
    
    # Initialize variables
    form_submitted = False
    form_data = {}
    errors = []
    
    # Check if this is a form submission (POST request)
    if request.method == 'POST':
        # Get form data from the request
        # request.POST is like a dictionary containing all form fields
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Store form data to repopulate form if there are errors
        form_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        
        # Simple validation (in real apps, you'd use Django forms for this)
        if not name:
            errors.append('Name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not message:
            errors.append('Message is required')
        
        # If no errors, process the form
        if not errors:
            # Here you would typically:
            # - Save to database
            # - Send email
            # - Redirect to success page
            # For this example, we'll just mark it as submitted
            form_submitted = True
            
            # Clear form data after successful submission
            form_data = {}
    
    # Prepare context for template
    context = {
        # Form handling
        'form_submitted': form_submitted,
        'form_data': form_data,
        'errors': errors,
        'is_post_request': request.method == 'POST',
        
        # Page info
        'page_title': 'Contact Us',
        'page_description': 'Get in touch with our team'
    }
    
    return render(request, 'examples/contact_form.html', context)

# =============================================================================
# EXAMPLE 7: SEARCH AND FILTERING
# =============================================================================

def search_view(request):
    """
    Shows how to handle search queries and filter results.
    This demonstrates working with GET parameters from search forms.
    
    GET PARAMETERS:
    When a user submits a search form, the data is sent in the URL like:
    /search/?q=django&category=tutorials
    """
    
    # Get search parameters from URL
    query = request.GET.get('q', '').strip()  # The search term
    category = request.GET.get('category', '')  # Filter by category
    sort_by = request.GET.get('sort', 'newest')  # Sort option
    
    # Start with all published articles
    articles = Article.objects.filter(is_published=True)
    
    # Apply search filter if query exists
    if query:
        # Search in title and content (case-insensitive)
        articles = articles.filter(
            title__icontains=query
        ) | articles.filter(
            content__icontains=query
        )
    
    # Apply sorting
    if sort_by == 'oldest':
        articles = articles.order_by('created_at')
    elif sort_by == 'title':
        articles = articles.order_by('title')
    else:  # newest (default)
        articles = articles.order_by('-created_at')
    
    # Get search statistics
    total_results = articles.count()
    
    # For better performance, only get the fields we need
    articles = articles.select_related('author')[:20]  # Limit to 20 results
    
    # Prepare search suggestions (if no results found)
    suggestions = []
    if query and total_results == 0:
        # Find articles with similar titles
        similar_articles = Article.objects.filter(
            title__icontains=query[:3],  # First 3 characters
            is_published=True
        )[:3]
        suggestions = [article.title for article in similar_articles]
    
    context = {
        # Search results
        'articles': articles,
        'total_results': total_results,
        'suggestions': suggestions,
        
        # Search parameters (to repopulate form)
        'query': query,
        'category': category,
        'sort_by': sort_by,
        
        # Search state
        'has_search': bool(query),
        'has_results': total_results > 0,
        'showing_all': not query and not category,
        
        # Page info
        'page_title': f'Search Results for "{query}"' if query else 'All Articles',
        'page_description': f'Found {total_results} articles matching your search'
    }
    
    return render(request, 'examples/search_results.html', context)

# =============================================================================
# HOW TO USE THESE EXAMPLES:
# =============================================================================
"""
To use these views, you need to:

1. ADD URL PATTERNS in your urls.py:
   
   from django.urls import path
   from . import views
   
   urlpatterns = [
       path('hello/', views.hello_world_view, name='hello_world'),
       path('data-types/', views.data_types_example_view, name='data_types'),
       path('database/', views.database_example_view, name='database_example'),
       path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
       path('article/<int:article_id>/', views.article_detail_view, name='article_detail'),
       path('contact/', views.contact_form_view, name='contact_form'),
       path('search/', views.search_view, name='search'),
   ]

2. CREATE TEMPLATES in your templates/examples/ directory:
   - hello_world.html
   - data_types.html
   - database_example.html
   - user_dashboard.html
   - article_detail.html
   - contact_form.html
   - search_results.html

3. IN YOUR TEMPLATES, access the data using Django template syntax:
   - Variables: {{ variable_name }}
   - Lists: {% for item in list_name %}{{ item }}{% endfor %}
   - Conditionals: {% if condition %}...{% endif %}
   - Dictionary values: {{ dict_name.key_name }}

REMEMBER:
- Views prepare the data
- Templates display the data
- The 'context' dictionary is the bridge between them
- Always validate user input in views, not templates
- Templates should be simple - do complex logic in views
"""

# =============================================================================
# TEMPLATE EXAMPLES FOR REFERENCE:
# =============================================================================
"""
Here are simple template examples for each view:

1. hello_world.html:
-------------------
{% extends 'base.html' %}
{% block content %}
    <h1>{{ greeting }}</h1>
    <p>Current time: {{ current_time }}</p>
    <p>App: {{ app_name }} v{{ version }}</p>
{% endblock %}

2. data_types.html:
------------------
{% extends 'base.html' %}
{% block content %}
    <h1>Hello, {{ user_name }}!</h1>
    <p>{{ welcome_message }}</p>
    
    {% if is_premium_user %}
        <p>🌟 You are a premium user!</p>
    {% endif %}
    
    <h3>Your Favorite Colors:</h3>
    <ul>
    {% for color in favorite_colors %}
        <li>{{ color }}</li>
    {% endfor %}
    </ul>
    
    <h3>Stats:</h3>
    <p>Posts: {{ user_stats.posts_count }}</p>
    <p>Followers: {{ user_stats.followers }}</p>
{% endblock %}

3. database_example.html:
------------------------
{% extends 'base.html' %}
{% block content %}
    <h1>Articles ({{ stats.published_articles }} published)</h1>
    
    {% for article in published_articles %}
        <div class="article">
            <h3>{{ article.title }}</h3>
            <p>By {{ article.author.username }} on {{ article.created_at|date:"F d, Y" }}</p>
            <p>{{ article.content|truncatewords:30 }}</p>
        </div>
    {% endfor %}
{% endblock %}
"""
