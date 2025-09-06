# Heroku Deployment Guide

This guide will walk you through deploying your Resume Generator Django app to Heroku.

## Prerequisites

1. **Heroku CLI** - Install from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. **Git** - Make sure your project is in a Git repository
3. **Heroku Account** - Sign up at [heroku.com](https://www.heroku.com)

## Step 1: Install Heroku CLI

### macOS (using Homebrew)
```bash
brew tap heroku/brew && brew install heroku
```

### Windows
Download and install from: https://devcenter.heroku.com/articles/heroku-cli

### Linux
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

## Step 2: Login to Heroku

```bash
heroku login
```

This will open a browser window for you to authenticate.

## Step 3: Create a Heroku App

```bash
# Navigate to your project directory
cd /Users/dheerajchand/Documents/Professional/resume_generator

# Create a new Heroku app
heroku create your-resume-generator-app-name

# Note: Replace 'your-resume-generator-app-name' with a unique name
# Heroku will assign a random name if you don't specify one
```

## Step 4: Set Environment Variables

```bash
# Set the secret key (generate a new one for production)
heroku config:set SECRET_KEY="your-super-secret-key-here"

# Set debug to False for production
heroku config:set DEBUG=False

# Set allowed hosts (Heroku will provide the domain)
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com,localhost,127.0.0.1"

# Optional: Set other environment variables
heroku config:set DJANGO_SETTINGS_MODULE="resume_generator_django.settings"
```

## Step 5: Deploy to Heroku

```bash
# Add Heroku remote (if not already added)
git remote add heroku https://git.heroku.com/your-app-name.git

# Deploy your code
git push heroku main

# If your main branch is called 'master', use:
# git push heroku master
```

## Step 6: Run Database Migrations

```bash
# Run migrations on Heroku
heroku run python manage.py migrate

# Create a superuser (optional)
heroku run python manage.py createsuperuser
```

## Step 7: Test Your Deployment

```bash
# Open your app in the browser
heroku open

# Check logs
heroku logs --tail
```

## Step 8: Generate Sample Resumes (Optional)

```bash
# Generate all resumes on Heroku
heroku run python manage.py generate_all_resumes --confirm
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `your-app.herokuapp.com` |
| `DATABASE_URL` | Database URL | Auto-set by Heroku |

## Troubleshooting

### Common Issues

1. **Build Fails**: Check `requirements.txt` for missing dependencies
2. **App Crashes**: Check logs with `heroku logs --tail`
3. **Static Files Not Loading**: Ensure `whitenoise` is in `MIDDLEWARE`
4. **Database Issues**: Run `heroku run python manage.py migrate`

### Useful Commands

```bash
# View app info
heroku info

# View environment variables
heroku config

# Access Heroku shell
heroku run bash

# Restart app
heroku restart

# Scale app (if needed)
heroku ps:scale web=1
```

## Production Considerations

1. **Security**: Set `DEBUG=False` and use a strong `SECRET_KEY`
2. **Database**: Consider upgrading to a paid database addon for production
3. **Static Files**: WhiteNoise is configured for static file serving
4. **Logging**: Logs are available via `heroku logs`
5. **Monitoring**: Consider adding monitoring tools like New Relic

## Next Steps

1. Set up a custom domain (optional)
2. Configure SSL (automatic with Heroku)
3. Set up monitoring and alerts
4. Consider using Heroku Postgres for production database
5. Set up automated deployments from GitHub

## Cost

- **Free Tier**: Limited hours per month, app sleeps after inactivity
- **Basic Tier**: $7/month for always-on app
- **Standard Tier**: $25/month for production features

Your app is already configured for Heroku with:
- ✅ `Procfile` for web process
- ✅ `requirements.txt` with all dependencies
- ✅ `runtime.txt` for Python version
- ✅ WhiteNoise for static files
- ✅ Environment variable configuration
- ✅ Database URL configuration
