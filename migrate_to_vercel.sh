#!/bin/bash

# Migration script for moving from SQLite to Vercel PostgreSQL
# Make sure to update config.properties with your Vercel database credentials first!

echo "🚀 Portfolio Builder - Database Migration to Vercel PostgreSQL"
echo "=============================================================="

# Check if config.properties exists
if [ ! -f "config.properties" ]; then
    echo "❌ Error: config.properties file not found!"
    echo "Please create config.properties with your database credentials."
    exit 1
fi

# Step 1: Backup current SQLite data
echo ""
echo "📦 Step 1: Creating backup of current SQLite data..."
python manage.py migrate_to_postgres --backup --dry-run

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create backup. Please check your Django setup."
    exit 1
fi

echo "✅ Backup created successfully!"

# Step 2: Check database connection
echo ""
echo "🔗 Step 2: Testing PostgreSQL connection..."
echo "Make sure you've added your POSTGRES_URL or NILEDB_POSTGRES_URL to config.properties"

read -p "Have you updated config.properties with your Vercel database URL? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please update config.properties first, then run this script again."
    echo ""
    echo "Add one of these lines to config.properties:"
    echo "POSTGRES_URL=your_postgres_url_from_vercel"
    echo "# OR"
    echo "NILEDB_POSTGRES_URL=your_niledb_postgres_url_from_vercel"
    exit 1
fi

python manage.py check --database default

if [ $? -ne 0 ]; then
    echo "❌ Error: Cannot connect to PostgreSQL database."
    echo "Please check your database URL in config.properties"
    exit 1
fi

echo "✅ Database connection successful!"

# Step 3: Run migrations
echo ""
echo "🏗️  Step 3: Creating database schema..."
python manage.py migrate --run-syncdb

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to run migrations."
    exit 1
fi

echo "✅ Database schema created!"

# Step 4: Initialize templates
echo ""
echo "🎨 Step 4: Initializing portfolio templates..."
python manage.py init_templates

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to initialize templates."
    exit 1
fi

echo "✅ Templates initialized!"

# Step 5: Final verification
echo ""
echo "🔍 Step 5: Verifying migration..."
python manage.py shell -c "
from core.models import PortfolioRequest, PortfolioTemplate
print(f'Portfolio Templates: {PortfolioTemplate.objects.count()}')
print('Available templates:')
for t in PortfolioTemplate.objects.all():
    print(f'  - {t.name} ({t.slug})')
print(f'Portfolio Requests: {PortfolioRequest.objects.count()}')
"

echo ""
echo "🎉 Migration completed successfully!"
echo ""
echo "Next steps:"
echo "1. Test your application: python manage.py runserver"
echo "2. Upload a test resume to verify everything works"
echo "3. Deploy to Vercel: vercel --prod"
echo ""
echo "📄 Your SQLite data backup is saved in: sqlite_backup.json"
echo "📖 For detailed instructions, see: MIGRATION_GUIDE.md"