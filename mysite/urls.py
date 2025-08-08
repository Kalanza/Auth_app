"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import (
    SignUpView, profile_view, UserListView, 
    admin_user_management, dashboard_view,
    custom_permission_denied_view
)

# Custom error handlers
handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Custom authentication views
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # User management views (require permissions)
    path('users/', UserListView.as_view(), name='user_list'),
    path('admin/users/', admin_user_management, name='admin_user_management'),
    
    # Redirect root to dashboard
    path('', dashboard_view, name='home'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
