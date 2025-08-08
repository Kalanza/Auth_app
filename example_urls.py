# =============================================================================
# SIMPLE URL CONFIGURATION FOR VIEWS TO TEMPLATES EXAMPLES
# =============================================================================
# This file shows how to connect your views to URLs so users can access them
# Add these patterns to your main urls.py or create a separate urls.py for your app
# =============================================================================

from django.urls import path
from . import complete_update_view_example as views

# URL patterns - these connect URLs to view functions
urlpatterns = [
    # =============================================================================
    # BASIC EXAMPLES
    # =============================================================================
    
    # Simple hello world example
    # URL: /hello/
    # This calls the hello_world_view function and renders hello_world.html
    path('hello/', views.hello_world_view, name='hello_world'),
    
    # Data types demonstration
    # URL: /data-types/
    # Shows different types of data being passed from view to template
    path('data-types/', views.data_types_example_view, name='data_types'),
    
    # Database example
    # URL: /database/
    # Demonstrates fetching data from the database and displaying it
    path('database/', views.database_example_view, name='database_example'),
    
    # User dashboard (requires login)
    # URL: /dashboard/
    # Shows personalized content for logged-in users
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
    
    # =============================================================================
    # DYNAMIC URLs WITH PARAMETERS
    # =============================================================================
    
    # Article detail with URL parameter
    # URL: /article/123/ (where 123 is the article ID)
    # The <int:article_id> captures the number from URL and passes it to the view
    path('article/<int:article_id>/', views.article_detail_view, name='article_detail'),
    
    # =============================================================================
    # FORM HANDLING
    # =============================================================================
    
    # Contact form (handles both GET and POST)
    # URL: /contact/
    # GET: displays the form, POST: processes the form submission
    path('contact/', views.contact_form_view, name='contact_form'),
    
    # Search functionality
    # URL: /search/ or /search/?q=django&sort=newest
    # Handles search queries from GET parameters
    path('search/', views.search_view, name='search'),
]

# =============================================================================
# HOW URLS WORK IN DJANGO:
# =============================================================================
"""
1. USER VISITS URL: When a user visits /hello/ in their browser

2. DJANGO MATCHES PATTERN: Django looks through urlpatterns and finds:
   path('hello/', views.hello_world_view, name='hello_world')

3. DJANGO CALLS VIEW: Django calls the hello_world_view function with the request

4. VIEW PROCESSES: The view function runs, prepares data, and calls render()

5. TEMPLATE RENDERS: Django combines the template with the data

6. RESPONSE SENT: The final HTML is sent back to the user's browser

THE FLOW:
URL → URL Pattern → View Function → Template → HTML Response

IMPORTANT CONCEPTS:

- path('url/', view_function, name='url_name')
  * 'url/' - the URL pattern users will visit
  * view_function - the Python function to call
  * name='url_name' - internal name for generating URLs

- <int:parameter> - captures integer from URL
- <str:parameter> - captures string from URL
- <slug:parameter> - captures slug (letters, numbers, hyphens, underscores)

- The 'name' parameter lets you use {% url 'name' %} in templates
- This makes your URLs maintainable - you can change the URL pattern
  without updating every template that links to it
"""

# =============================================================================
# EXAMPLE: HOW TO INCLUDE THESE URLS IN YOUR MAIN PROJECT
# =============================================================================
"""
In your main project's urls.py (mysite/urls.py), add:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include all the example URLs under /examples/ prefix
    path('examples/', include('myapp.example_urls')),
    
    # Or include them without prefix (directly in root)
    path('', include('myapp.example_urls')),
]

This means:
- If you use path('examples/', include(...)), URLs become:
  /examples/hello/, /examples/data-types/, etc.
  
- If you use path('', include(...)), URLs become:
  /hello/, /data-types/, etc.
"""

# =============================================================================
# TEMPLATE URL GENERATION EXAMPLES:
# =============================================================================
"""
In your templates, you can create links using the 'name' from urlpatterns:

<!-- Simple link -->
<a href="{% url 'hello_world' %}">Hello World</a>

<!-- Link with parameter -->
<a href="{% url 'article_detail' article.id %}">Read Article</a>

<!-- Form action -->
<form method="post" action="{% url 'contact_form' %}">
    {% csrf_token %}
    <!-- form fields -->
</form>

<!-- Search form -->
<form method="get" action="{% url 'search' %}">
    <input type="text" name="q" placeholder="Search...">
    <button type="submit">Search</button>
</form>

This is better than hardcoding URLs because:
- If you change the URL pattern, all links update automatically
- No broken links when you reorganize your URLs
- More maintainable code
"""
