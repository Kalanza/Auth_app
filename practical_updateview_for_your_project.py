# practical_updateview_for_your_project.py
# UpdateView examples using your existing models

from django.views.generic import UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import UserProfile, Article

# 1. User Profile Update View
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allow users to update their own profile information.
    
    This view demonstrates:
    - User-specific data access
    - Custom success URL
    - Permission checking
    - Custom form validation
    """
    model = UserProfile
    fields = ['phone_number', 'birth_date', 'bio', 'location', 'avatar']
    template_name = 'accounts/profile_update.html'
    
    def get_object(self, queryset=None):
        """Always return the current user's profile."""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_success_url(self):
        """Redirect back to the user's profile page."""
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
    
    def form_valid(self, form):
        """Add success message and custom logic."""
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Your profile has been updated successfully!'
        )
        return response
    
    def get_context_data(self, **kwargs):
        """Add extra context for the template."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update My Profile'
        context['user'] = self.request.user
        return context

# 2. Article Update View with Permission Checking
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow users to update their own articles, or admins to update any article.
    
    This view demonstrates:
    - Permission checking
    - Different field access based on user type
    - Custom success messages
    """
    model = Article
    template_name = 'articles/article_update.html'
    
    def test_func(self):
        """Check if user has permission to edit this article."""
        article = self.get_object()
        return (
            # Author can edit their own article
            article.author == self.request.user or
            # Staff can edit any article
            self.request.user.is_staff or
            # Users with specific permission can edit
            self.request.user.has_perm('myapp.can_edit_all_articles')
        )
    
    def get_form_class(self):
        """Return different forms based on user permissions."""
        if self.request.user.is_staff or self.request.user.has_perm('myapp.can_publish_article'):
            # Staff and publishers can edit all fields including published status
            fields = ['title', 'content', 'is_published']
        else:
            # Regular authors can only edit title and content
            fields = ['title', 'content']
        
        from django.forms import modelform_factory
        return modelform_factory(Article, fields=fields)
    
    def form_valid(self, form):
        """Custom validation and success handling."""
        # Don't change the author when updating
        form.instance.author = self.get_object().author
        
        response = super().form_valid(form)
        
        # Custom success message
        if form.cleaned_data.get('is_published', False):
            messages.success(
                self.request,
                f'Article "{self.object.title}" has been updated and is now published!'
            )
        else:
            messages.success(
                self.request,
                f'Article "{self.object.title}" has been updated successfully!'
            )
        
        return response
    
    def get_success_url(self):
        """Redirect to the article detail page."""
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

# 3. Admin-Only User Update View
class AdminUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow admins to update any user's basic information.
    
    This view demonstrates:
    - Admin-only access
    - Updating User model (not just custom models)
    - Security considerations
    """
    model = User
    fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']
    template_name = 'admin/user_update.html'
    success_url = reverse_lazy('user_list')
    
    def test_func(self):
        """Only superusers can access this view."""
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        """Add logging and validation for admin changes."""
        original_user = User.objects.get(pk=self.object.pk)
        response = super().form_valid(form)
        
        # Log important changes
        if original_user.is_staff != self.object.is_staff:
            from django.contrib.admin.models import LogEntry, CHANGE
            from django.contrib.contenttypes.models import ContentType
            
            LogEntry.objects.create(
                user_id=self.request.user.pk,
                content_type=ContentType.objects.get_for_model(User),
                object_id=self.object.pk,
                object_repr=str(self.object),
                action_flag=CHANGE,
                change_message=f'Staff status changed by {self.request.user.username}'
            )
        
        messages.success(
            self.request,
            f'User {self.object.username} has been updated successfully!'
        )
        
        return response

# 4. Bulk Update View (Advanced Pattern)
class BulkArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow users to update multiple articles at once.
    This is a more advanced pattern.
    """
    model = Article
    fields = ['is_published']
    template_name = 'articles/bulk_update.html'
    
    def test_func(self):
        """Only staff can do bulk updates."""
        return self.request.user.is_staff
    
    def post(self, request, *args, **kwargs):
        """Handle bulk update logic."""
        article_ids = request.POST.getlist('article_ids')
        action = request.POST.get('action')
        
        if action == 'publish':
            Article.objects.filter(
                id__in=article_ids
            ).update(is_published=True)
            messages.success(request, f'{len(article_ids)} articles published!')
        elif action == 'unpublish':
            Article.objects.filter(
                id__in=article_ids
            ).update(is_published=False)
            messages.success(request, f'{len(article_ids)} articles unpublished!')
        
        return redirect('article_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context

# Template Examples for your views:

# templates/accounts/profile_update.html
profile_template = '''
{% extends 'base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
<div class="container">
    <h2>{{ page_title }}</h2>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label>Phone Number:</label>
                    {{ form.phone_number }}
                </div>
                
                <div class="form-group">
                    <label>Birth Date:</label>
                    {{ form.birth_date }}
                </div>
                
                <div class="form-group">
                    <label>Location:</label>
                    {{ form.location }}
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="form-group">
                    <label>Bio:</label>
                    {{ form.bio }}
                </div>
                
                <div class="form-group">
                    <label>Avatar:</label>
                    {{ form.avatar }}
                    {% if object.avatar %}
                        <img src="{{ object.avatar.url }}" alt="Current avatar" width="100">
                    {% endif %}
                </div>
            </div>
        </div>
        
        <button type="submit" class="btn btn-primary">Update Profile</button>
        <a href="{% url 'profile' user.pk %}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
{% endblock %}
'''

# URL patterns to add to your urls.py:
url_patterns = '''
# Add these to your myapp/urls.py:
from django.urls import path
from . import views

urlpatterns = [
    # Profile management
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    
    # Article management
    path('articles/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    
    # Admin views
    path('admin/users/<int:pk>/update/', views.AdminUserUpdateView.as_view(), name='admin_user_update'),
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
]
'''

# What happens in the browser:
"""
1. User visits /profile/update/
2. Django loads UserProfileUpdateView
3. get_object() gets or creates the user's profile
4. A form is displayed with current profile data
5. User changes some fields and submits
6. Django validates the form
7. If valid: form_valid() runs, saves data, adds message, redirects
8. If invalid: form_invalid() runs, shows errors
"""

# Key Takeaways for Junior Developers:
"""
1. UpdateView handles 90% of the work for you
2. You just configure which model, fields, and template to use
3. Override methods only when you need custom behavior
4. Always consider security - who can edit what?
5. Use mixins like LoginRequiredMixin for common requirements
6. Add success messages to give users feedback
7. Use reverse_lazy for URLs in class attributes
8. Test your permission logic thoroughly!
"""
