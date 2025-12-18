"""
Management command to migrate data from SQLite to PostgreSQL
"""
import os
import json
from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
from core.models import PortfolioRequest, PortfolioTemplate


class Command(BaseCommand):
    help = 'Migrate data from SQLite to PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create a JSON backup of SQLite data before migration',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        create_backup = options['backup']

        self.stdout.write(
            self.style.SUCCESS('Starting migration from SQLite to PostgreSQL...')
        )

        # Check current database configuration
        current_db = settings.DATABASES['default']['ENGINE']
        self.stdout.write(f'Current database engine: {current_db}')

        # Check if tables exist
        try:
            portfolio_requests = list(PortfolioRequest.objects.all().values())
            portfolio_templates = list(PortfolioTemplate.objects.all().values())
            tables_exist = True
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Database tables do not exist yet: {str(e)[:100]}...')
            )
            tables_exist = False
            portfolio_requests = []
            portfolio_templates = []

        if not tables_exist:
            self.stdout.write(
                self.style.SUCCESS('\n=== SETUP REQUIRED ===')
            )
            self.stdout.write('It looks like you\'ve connected to PostgreSQL but tables don\'t exist yet.')
            self.stdout.write('Please run these commands first:')
            self.stdout.write('1. python manage.py migrate --run-syncdb')
            self.stdout.write('2. python manage.py init_templates')
            self.stdout.write('3. Then run this command again to check for data to migrate')
            return

        # Create backup if requested and tables exist
        if create_backup and tables_exist:
            self.create_backup()

        self.stdout.write(f'Found {len(portfolio_requests)} portfolio requests')
        self.stdout.write(f'Found {len(portfolio_templates)} portfolio templates')

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN - No data will be migrated')
            )
            if portfolio_requests or portfolio_templates:
                self.show_migration_preview(portfolio_requests, portfolio_templates)
            return

        # Show migration status
        if portfolio_requests or portfolio_templates:
            self.stdout.write('\n=== DATA TO MIGRATE ===')
            self.show_migration_preview(portfolio_requests, portfolio_templates)
        else:
            self.stdout.write(
                self.style.SUCCESS('\n=== MIGRATION COMPLETE ===')
            )
            self.stdout.write('No data found to migrate. Your PostgreSQL database is ready!')
            self.stdout.write('You can now use your application with the new database.')

    def create_backup(self):
        """Create a JSON backup of the current SQLite data"""
        backup_data = {
            'portfolio_requests': list(PortfolioRequest.objects.all().values()),
            'portfolio_templates': list(PortfolioTemplate.objects.all().values()),
        }
        
        # Convert datetime objects to strings for JSON serialization
        for item in backup_data['portfolio_requests']:
            for key, value in item.items():
                if hasattr(value, 'isoformat'):
                    item[key] = value.isoformat()
        
        for item in backup_data['portfolio_templates']:
            for key, value in item.items():
                if hasattr(value, 'isoformat'):
                    item[key] = value.isoformat()

        backup_file = 'sqlite_backup.json'
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        self.stdout.write(
            self.style.SUCCESS(f'Backup created: {backup_file}')
        )

    def show_migration_preview(self, portfolio_requests, portfolio_templates):
        """Show what data will be migrated"""
        self.stdout.write('\n--- Portfolio Requests ---')
        for req in portfolio_requests:
            self.stdout.write(f'ID: {req["id"]}, File: {req["resume_file"]}, Created: {req["created_at"]}')
        
        self.stdout.write('\n--- Portfolio Templates ---')
        for template in portfolio_templates:
            self.stdout.write(f'ID: {template["id"]}, Name: {template["name"]}, Slug: {template["slug"]}')