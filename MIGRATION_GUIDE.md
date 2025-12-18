# Database Migration Guide: SQLite to Vercel PostgreSQL

This guide will help you migrate your local SQLite data to Vercel's PostgreSQL database.

## Prerequisites

1. ✅ You have Vercel database credentials (shown in your screenshot)
2. ✅ Your project has `psycopg2-binary` and `dj-database-url` in requirements.txt
3. ✅ Your Django settings are configured to read database URLs

## Step 1: Backup Your Current Data

First, let's create a backup of your current SQLite data:

```bash
python manage.py migrate_to_postgres --backup --dry-run
```

This will:
- Show you what data exists in your current database
- Create a `sqlite_backup.json` file with all your data

## Step 2: Configure Vercel Database Connection

You need to add your Vercel database credentials to `config.properties`. Based on your screenshot, you have these environment variables:

- `POSTGRES_URL`
- `NILEDB_PASSWORD` 
- `NILEDB_API_URL`
- `NILEDB_POSTGRES_URL`
- `NILEDB_USER`
- `NILEDB_URL`

### Option A: Using POSTGRES_URL (Standard Vercel Postgres)

Edit `config.properties` and add:
```properties
POSTGRES_URL=your_postgres_url_value_here
```

### Option B: Using NileDB (If you're using Nile)

Edit `config.properties` and add:
```properties
NILEDB_POSTGRES_URL=your_niledb_postgres_url_value_here
```

**Important:** Copy the actual URL values from your Vercel dashboard, not the variable names.

## Step 3: Test Database Connection

Test that Django can connect to your PostgreSQL database:

```bash
python manage.py check --database default
```

If successful, you should see: "System check identified no issues"

## Step 4: Run Migrations on PostgreSQL

Create the database schema on your PostgreSQL database:

```bash
python manage.py migrate --run-syncdb
```

This creates all the necessary tables in your PostgreSQL database.

## Step 5: Initialize Templates

Recreate the portfolio templates in the new database:

```bash
python manage.py init_templates
```

## Step 6: Migrate Your Data (Manual Method)

Since you likely have important portfolio requests, you'll need to manually recreate them. The backup file created in Step 1 contains all your data.

### If you have portfolio requests to migrate:

1. Check your backup file `sqlite_backup.json`
2. For each portfolio request, you can either:
   - Re-upload the PDF files through the web interface, or
   - Use Django shell to recreate the records

### Using Django Shell (Advanced):

```bash
python manage.py shell
```

Then in the shell:
```python
import json
from core.models import PortfolioRequest

# Load backup data
with open('sqlite_backup.json', 'r') as f:
    backup = json.load(f)

# Recreate portfolio requests
for req_data in backup['portfolio_requests']:
    # Remove the old ID to let Django create a new one
    req_data.pop('id', None)
    
    # Create new record
    PortfolioRequest.objects.create(**req_data)
    print(f"Migrated: {req_data['resume_file']}")
```

## Step 7: Verify Migration

Check that everything migrated correctly:

```bash
python manage.py shell
```

```python
from core.models import PortfolioRequest, PortfolioTemplate

print(f"Portfolio Requests: {PortfolioRequest.objects.count()}")
print(f"Portfolio Templates: {PortfolioTemplate.objects.count()}")

# List all templates
for template in PortfolioTemplate.objects.all():
    print(f"- {template.name} ({template.slug})")
```

## Step 8: Update Your Application

Once migration is complete:

1. **Remove SQLite file** (optional): `rm db.sqlite3`
2. **Test your application**: `python manage.py runserver`
3. **Try uploading a new resume** to ensure everything works

## Step 9: Deploy to Vercel

Your application is now ready for Vercel deployment:

```bash
# If you haven't already
vercel --prod
```

## Troubleshooting

### Connection Issues

If you get connection errors:

1. **Check your database URL format**:
   - Should start with `postgresql://` (not `postgres://`)
   - Django settings automatically converts `postgres://` to `postgresql://`

2. **Verify credentials**:
   - Copy the exact values from Vercel dashboard
   - Don't include quotes around the URL

3. **Check network access**:
   - Ensure your local machine can reach Vercel's database
   - Some corporate networks block external database connections

### Migration Issues

If data migration fails:

1. **Check the backup file**: `sqlite_backup.json` contains all your data
2. **Manual recreation**: You can always re-upload PDFs through the web interface
3. **File paths**: Resume files in `media/resumes/` need to be uploaded again

### Template Issues

If templates are missing:

```bash
python manage.py init_templates
```

This recreates the three default templates (Terminal, Renaissance, Newspaper).

## Environment Variables for Production

For Vercel deployment, make sure these environment variables are set in your Vercel dashboard:

- `POSTGRES_URL` (or `NILEDB_POSTGRES_URL`)
- `GEMINI_API_KEY`
- `FIREBASE_API_KEY` (if using Firebase)
- Any other credentials from your `config.properties`

## Quick Commands Summary

```bash
# 1. Backup current data
python manage.py migrate_to_postgres --backup --dry-run

# 2. Test connection (after updating config.properties)
python manage.py check --database default

# 3. Create PostgreSQL schema
python manage.py migrate --run-syncdb

# 4. Initialize templates
python manage.py init_templates

# 5. Test application
python manage.py runserver
```

## Need Help?

If you encounter issues:

1. Check the backup file was created successfully
2. Verify your database URL is correct
3. Ensure all required packages are installed
4. Test the connection with a simple Django shell command

The most important thing is that your data is backed up in `sqlite_backup.json`, so you can always recover if something goes wrong.