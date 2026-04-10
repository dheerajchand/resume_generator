# Deployment Guide

The Resume Generator is hosted on [Railway](https://railway.app/) at:

**https://dheeraj-chands-resume-generator-production.up.railway.app**

---

## Railway Architecture

Railway provides:
- **Web service** — Runs the Django application from the Dockerfile.
- **PostgreSQL 16** — Managed database provisioned as a Railway plugin.
- **Automatic deploys** — Triggered on push to the configured branch.

---

## Environment Variables

All configuration is managed through Railway's environment variable system. Navigate to your project's **Variables** tab in the Railway dashboard.

### Required Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `a-long-random-string` | Django secret key. Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` | **Must be `False` in production.** |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/dbname` | Automatically set by Railway when you provision a PostgreSQL plugin. Do not set manually. |
| `DJANGO_SETTINGS_MODULE` | `config.settings` | Python path to the settings module. |
| `ALLOWED_HOSTS` | `dheeraj-chands-resume-generator-production.up.railway.app` | Comma-separated hostnames. Must include the Railway domain. |

### Email Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `RESEND_API_KEY` | `re_xxxxxxxxx` | API key from [Resend](https://resend.com/). Required for sending resumes via email. |
| `FROM_EMAIL` | `resumes@yourdomain.com` | The sender email address. Must be verified in Resend. |

### Optional Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://default:pass@host:6379` | Redis connection URL. If set, Django uses Redis for caching. If not set, falls back to Django's default in-memory cache. |

---

## Initial Deployment

### 1. Create Railway Project

1. Log in to [Railway](https://railway.app/).
2. Click **New Project**.
3. Select **Deploy from GitHub repo** and connect your repository.
4. Railway will detect the Dockerfile and configure the build.

### 2. Provision PostgreSQL

1. In your Railway project, click **New** > **Database** > **PostgreSQL**.
2. Railway automatically sets the `DATABASE_URL` environment variable.
3. Wait for the database to be ready.

### 3. Set Environment Variables

1. Click on your web service.
2. Go to the **Variables** tab.
3. Add all required variables listed above.

### 4. Deploy

1. Railway deploys automatically on push to the configured branch.
2. Or click **Deploy** manually in the Railway dashboard.

### 5. Run Initial Migrations

1. Open the Railway **Shell** (click on the web service > **Shell** tab).
2. Run:
   ```bash
   python manage.py migrate
   ```

### 6. Create Superuser

In the Railway shell:
```bash
python manage.py createsuperuser
```

### 7. Load Data

In the Railway shell:
```bash
python manage.py import_master_data
```

---

## Redeployment

### Automatic Deploys

Railway redeploys automatically when you push to the configured branch (typically `main`). The process:

1. Railway detects the push.
2. Builds a new Docker image from the Dockerfile.
3. Runs the new container.
4. Switches traffic to the new container (zero-downtime).

### Manual Deploy

1. Go to the Railway dashboard.
2. Click on your web service.
3. Click **Deploy** or trigger a redeploy from the **Deployments** tab.

### After Deploy Checklist

If your deploy includes model changes:

1. Open the Railway shell.
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Verify the admin loads correctly.
4. Test resume generation from the public form.

---

## Database Management

### Accessing the Database

**Via Railway Shell:**
```bash
python manage.py dbshell
```

**Via Django ORM (Railway Shell):**
```bash
python manage.py shell
>>> from portfolio.models import PersonalInfo
>>> PersonalInfo.objects.first()
```

### Backups

Railway's PostgreSQL plugin provides automated backups. You can also create manual backups:

**Export:**
```bash
# From Railway shell or local machine with DATABASE_URL set
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

**Import:**
```bash
psql $DATABASE_URL < backup_20260410.sql
```

### Data Loading

To reload seed data (this updates existing records and creates missing ones):
```bash
python manage.py import_master_data
```

---

## Domain Configuration

### Custom Domain

1. In Railway, click on your web service.
2. Go to **Settings** > **Networking** > **Custom Domain**.
3. Add your domain.
4. Configure DNS (CNAME record pointing to Railway's domain).
5. Update `ALLOWED_HOSTS` to include the custom domain.

### HTTPS

Railway provides automatic HTTPS via Let's Encrypt for both the default `*.up.railway.app` domain and custom domains.

---

## Monitoring

### Logs

1. Click on your web service in Railway.
2. Go to the **Logs** tab.
3. View real-time application logs.

### Health Checks

Railway monitors the health of your service. If the container crashes, it restarts automatically.

You can also run smoke tests:
```bash
# From Railway shell
python manage.py smoke_test_urls
```

---

## Troubleshooting

### "DisallowedHost" Error

The request's hostname is not in `ALLOWED_HOSTS`. Add it to the environment variable.

### Database Connection Errors

1. Check that the PostgreSQL plugin is running in Railway.
2. Verify `DATABASE_URL` is set (Railway should set this automatically).
3. Try restarting the web service.

### Static Files Not Loading

Ensure `collectstatic` runs during the Docker build or as part of the startup command. Check the Dockerfile for a `collectstatic` step.

### Email Sending Fails

1. Verify `RESEND_API_KEY` is set and valid.
2. Verify `FROM_EMAIL` is verified in Resend's dashboard.
3. Check application logs for error details.

### Memory Issues

If the container runs out of memory during PDF generation:
1. Check Railway's resource usage graphs.
2. Consider upgrading the Railway plan for more memory.
3. Review ReportLab usage for memory-intensive operations.
