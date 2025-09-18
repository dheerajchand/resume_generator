#!/usr/bin/env python3
"""
Heroku Deployment Script for Resume Generator
Automates the deployment process with proper configuration
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    print(f"   Command: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
    else:
        print(f"❌ {description} failed")
        print(f"   Error: {result.stderr.strip()}")
        return False
    
    return True


def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    result = subprocess.run("heroku --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("❌ Heroku CLI not found. Please install it first:")
        print("   https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    print("✅ Heroku CLI found")
    return True


def check_git_status():
    """Check if git repo is clean"""
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  Git working directory is not clean:")
        print(result.stdout)
        response = input("Continue anyway? (y/N): ")
        return response.lower() == 'y'
    
    print("✅ Git working directory is clean")
    return True


def main():
    """Main deployment function"""
    print("🚀 Resume Generator Heroku Deployment Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_heroku_cli():
        sys.exit(1)
    
    if not check_git_status():
        sys.exit(1)
    
    # Get app name
    app_name = input("Enter your Heroku app name (or press Enter to create a new one): ").strip()
    
    if not app_name:
        app_name = input("Enter a name for your new Heroku app: ").strip()
        if not app_name:
            print("❌ App name is required")
            sys.exit(1)
        
        # Create new Heroku app
        if not run_command(f"heroku create {app_name}", "Creating Heroku app"):
            sys.exit(1)
    
    # Add Heroku remote if it doesn't exist
    run_command(f"heroku git:remote -a {app_name}", "Adding Heroku remote")
    
    # Add PostgreSQL addon
    if not run_command(f"heroku addons:create heroku-postgresql:essential-0 -a {app_name}", "Adding PostgreSQL database"):
        print("ℹ️  PostgreSQL addon might already exist")
    
    # Add Redis addon (optional, for better performance)
    response = input("Add Redis for caching? (y/N): ")
    if response.lower() == 'y':
        if not run_command(f"heroku addons:create heroku-redis:mini -a {app_name}", "Adding Redis cache"):
            print("ℹ️  Redis addon might already exist")
    
    # Set environment variables
    print("\n🔧 Setting environment variables...")
    
    # Generate a secret key
    secret_key = input("Enter a secret key (or press Enter to generate one): ").strip()
    if not secret_key:
        import secrets
        secret_key = secrets.token_urlsafe(50)
        print(f"Generated secret key: {secret_key[:20]}...")
    
    env_vars = {
        'SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'DJANGO_SETTINGS_MODULE': 'resume_generator_django.settings_production',
        'RESUME_GENERATION_TIMEOUT': '300',
        'MAX_CONCURRENT_GENERATIONS': '5',
        'ENABLE_RESUME_CACHING': 'True',
    }
    
    for key, value in env_vars.items():
        run_command(f"heroku config:set {key}='{value}' -a {app_name}", f"Setting {key}")
    
    # Deploy to Heroku
    print("\n🚀 Deploying to Heroku...")
    if not run_command("git push heroku HEAD:main", "Deploying code to Heroku"):
        print("❌ Deployment failed")
        sys.exit(1)
    
    # Run migrations
    if not run_command(f"heroku run python manage.py migrate -a {app_name}", "Running database migrations"):
        print("❌ Migration failed")
        sys.exit(1)
    
    # Create superuser (optional)
    response = input("Create a superuser account? (y/N): ")
    if response.lower() == 'y':
        run_command(f"heroku run python manage.py createsuperuser -a {app_name}", "Creating superuser")
    
    # Setup resume system
    if not run_command(f"heroku run python manage.py setup_resume_system -a {app_name}", "Setting up resume system"):
        print("ℹ️  Resume system setup might have failed - check logs")
    
    # Open the app
    print(f"\n🎉 Deployment complete!")
    print(f"🌐 Your app is available at: https://{app_name}.herokuapp.com")
    
    response = input("Open the app in your browser? (y/N): ")
    if response.lower() == 'y':
        run_command(f"heroku open -a {app_name}", "Opening app in browser")
    
    print("\n📋 Next steps:")
    print("1. Visit your app URL to test functionality")
    print("2. Login to admin at /admin/ with your superuser account")
    print("3. Upload your personal resume data")
    print("4. Generate your first resume!")
    
    print(f"\n🔧 Useful Heroku commands:")
    print(f"   heroku logs --tail -a {app_name}  # View logs")
    print(f"   heroku run python manage.py shell -a {app_name}  # Django shell")
    print(f"   heroku restart -a {app_name}  # Restart app")


if __name__ == "__main__":
    main()
