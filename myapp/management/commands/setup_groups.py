from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import Article, UserProfile

class Command(BaseCommand):
    """
    Management command to set up user groups and permissions
    Usage: python manage.py setup_groups
    """
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **options):
        self.stdout.write('Creating groups and assigning permissions...')

        # Create groups
        groups_data = {
            'Site Admins': 'Full administrative access',
            'Moderators': 'Content moderation and user management',
            'Authors': 'Can create and publish articles',
            'Members': 'Basic user access'
        }

        created_groups = {}
        for group_name, description in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            created_groups[group_name] = group
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(f'Group already exists: {group_name}')

        # Get content types
        article_ct = ContentType.objects.get_for_model(Article)
        profile_ct = ContentType.objects.get_for_model(UserProfile)

        # Site Admins - all permissions
        admin_group = created_groups['Site Admins']
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)
        self.stdout.write('Assigned all permissions to Site Admins')

        # Moderators - content and profile management
        moderator_group = created_groups['Moderators']
        moderator_permissions = Permission.objects.filter(
            content_type__in=[article_ct, profile_ct]
        )
        moderator_group.permissions.set(moderator_permissions)
        self.stdout.write('Assigned moderation permissions to Moderators')

        # Authors - article creation and publishing
        author_group = created_groups['Authors']
        author_permissions = Permission.objects.filter(
            codename__in=[
                'add_article', 'change_article', 'delete_article',
                'can_publish_article', 'can_unpublish_article'
            ]
        )
        author_group.permissions.set(author_permissions)
        self.stdout.write('Assigned author permissions to Authors')

        # Members - basic permissions
        member_group = created_groups['Members']
        member_permissions = Permission.objects.filter(
            codename__in=['add_article', 'change_article']
        )
        member_group.permissions.set(member_permissions)
        self.stdout.write('Assigned basic permissions to Members')

        self.stdout.write(
            self.style.SUCCESS('Successfully set up all groups and permissions!')
        )
