#!/usr/bin/env python
"""
Django User Management System - Setup Script
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a system command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Django User Management System - Setup")
    print("=" * 50)
    
    # Check if manage.py exists
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Are you in the correct directory?")
        sys.exit(1)
    
    print("📦 Installing dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    print("\n🗃️  Setting up database...")
    if not run_command("python manage.py makemigrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate"):
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    print("\n👥 Setting up user groups and permissions...")
    if not run_command("python manage.py setup_groups"):
        print("❌ Failed to setup groups")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Visit: http://127.0.0.1:8000")
    print("\nFor learning examples, visit:")
    print("- /hello/ - Basic data passing")
    print("- /data-types/ - Template patterns")
    print("- /database/ - Database examples")
    print("- /dashboard/ - User dashboard (after login)")

if __name__ == "__main__":
    main()
