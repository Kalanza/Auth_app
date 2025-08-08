from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    """
    Extended user profile model to store additional user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_view_all_profiles", "Can view all user profiles"),
            ("can_edit_all_profiles", "Can edit all user profiles"),
            ("can_delete_profiles", "Can delete user profiles"),
        ]

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Article(models.Model):
    """
    Sample content model to demonstrate permissions
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_publish_article", "Can publish articles"),
            ("can_unpublish_article", "Can unpublish articles"),
            ("can_view_unpublished", "Can view unpublished articles"),
        ]

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserProfile when a User is created
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile when the User is saved
    """
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

def create_groups_and_permissions():
    """
    Function to create custom groups and assign permissions
    This should be run after migrations
    """
    # Create groups
    admin_group, created = Group.objects.get_or_create(name='Site Admins')
    moderator_group, created = Group.objects.get_or_create(name='Moderators')
    author_group, created = Group.objects.get_or_create(name='Authors')
    member_group, created = Group.objects.get_or_create(name='Members')

    # Get content types
    article_ct = ContentType.objects.get_for_model(Article)
    profile_ct = ContentType.objects.get_for_model(UserProfile)

    # Assign permissions to groups
    # Site Admins - all permissions
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # Moderators - can manage content and profiles
    moderator_permissions = Permission.objects.filter(
        content_type__in=[article_ct, profile_ct]
    )
    moderator_group.permissions.set(moderator_permissions)

    # Authors - can create and edit their own articles
    author_permissions = Permission.objects.filter(
        codename__in=['add_article', 'change_article', 'can_publish_article']
    )
    author_group.permissions.set(author_permissions)

    # Members - basic permissions
    member_permissions = Permission.objects.filter(
        codename__in=['add_article', 'change_article']
    )
    member_group.permissions.set(member_permissions)
