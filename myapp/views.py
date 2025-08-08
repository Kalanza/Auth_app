from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.db import transaction
from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm
from .models import UserProfile, Article

class SignUpView(CreateView):
    """
    Enhanced user registration view
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """
        Override form_valid to add user to default group and show success message
        """
        response = super().form_valid(form)
        
        # Add user to default 'Members' group
        members_group, created = Group.objects.get_or_create(name='Members')
        self.object.groups.add(members_group)
        
        messages.success(
            self.request, 
            f'Account created successfully for {self.object.username}! You can now log in.'
        )
        return response

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Account'
        return context

@login_required
def profile_view(request):
    """
    User profile view that displays and allows editing of profile information
    """
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'title': 'My Profile'
    }
    return render(request, 'accounts/profile.html', context)

class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View to list all users (requires special permission)
    """
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    permission_required = 'myapp.can_view_all_profiles'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.all().select_related('userprofile')

@permission_required('myapp.can_edit_all_profiles')
def admin_user_management(request):
    """
    Admin view for managing users and their groups
    """
    users = User.objects.all().prefetch_related('groups', 'userprofile')
    groups = Group.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        action = request.POST.get('action')
        
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(id=group_id)
            
            if action == 'add':
                user.groups.add(group)
                messages.success(request, f'Added {user.username} to {group.name}')
            elif action == 'remove':
                user.groups.remove(group)
                messages.success(request, f'Removed {user.username} from {group.name}')
                
        except (User.DoesNotExist, Group.DoesNotExist):
            messages.error(request, 'User or group not found')
        
        return redirect('admin_user_management')
    
    context = {
        'users': users,
        'groups': groups,
        'title': 'User Management'
    }
    return render(request, 'accounts/admin_user_management.html', context)

@login_required
def dashboard_view(request):
    """
    Main dashboard view showing user-specific content based on permissions
    """
    user = request.user
    context = {
        'title': 'Dashboard',
        'user_groups': user.groups.all(),
        'user_permissions': user.get_all_permissions(),
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    }
    
    # Add different content based on user permissions
    if user.has_perm('myapp.can_view_all_profiles'):
        context['can_view_all_profiles'] = True
        context['total_users'] = User.objects.count()
    
    if user.has_perm('myapp.can_publish_article'):
        context['can_publish_articles'] = True
        context['total_articles'] = Article.objects.count()
    
    return render(request, 'accounts/dashboard.html', context)

def custom_permission_denied_view(request, exception):
    """
    Custom 403 permission denied view
    """
    return render(request, 'errors/403.html', status=403)
