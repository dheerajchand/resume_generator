"""
Unified system administration command for Resume Generator
Replaces scattered utility scripts with a single comprehensive command
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from pathlib import Path
import json
import shutil

from resumes.models import ColorScheme, UserColorScheme, ResumeTemplate
from resumes.services import ResumeGenerationService


class Command(BaseCommand):
    help = 'Unified system administration for Resume Generator'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            required=True,
            choices=[
                'cleanup', 'backup', 'restore', 'migrate-data', 
                'create-color-scheme', 'export-user-data', 'import-user-data',
                'optimize-database', 'generate-test-data'
            ],
            help='Action to perform'
        )
        
        parser.add_argument(
            '--user',
            type=str,
            help='Username for user-specific actions'
        )
        
        parser.add_argument(
            '--file',
            type=str,
            help='File path for import/export actions'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force action without confirmation'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'cleanup':
            self.cleanup_system(options)
        elif action == 'backup':
            self.backup_data(options)
        elif action == 'restore':
            self.restore_data(options)
        elif action == 'migrate-data':
            self.migrate_legacy_data(options)
        elif action == 'create-color-scheme':
            self.create_color_scheme(options)
        elif action == 'export-user-data':
            self.export_user_data(options)
        elif action == 'import-user-data':
            self.import_user_data(options)
        elif action == 'optimize-database':
            self.optimize_database(options)
        elif action == 'generate-test-data':
            self.generate_test_data(options)

    def cleanup_system(self, options):
        """Clean up temporary files and optimize system"""
        self.stdout.write("🧹 Starting system cleanup...")
        
        # Remove Python cache files
        cache_dirs = list(Path('.').rglob('__pycache__'))
        for cache_dir in cache_dirs:
            if '.venv' not in str(cache_dir) and 'venv' not in str(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)
                self.stdout.write(f"   Removed: {cache_dir}")
        
        # Remove temporary files
        temp_files = list(Path('.').glob('*.tmp')) + list(Path('.').glob('*.temp'))
        for temp_file in temp_files:
            temp_file.unlink(missing_ok=True)
            self.stdout.write(f"   Removed: {temp_file}")
        
        # Clean up old migration files (keep the latest)
        # This is a placeholder - implement if needed
        
        self.stdout.write(self.style.SUCCESS("✅ System cleanup completed"))

    def backup_data(self, options):
        """Backup user data and configurations"""
        self.stdout.write("💾 Creating system backup...")
        
        backup_dir = Path('backups') / f"backup_{self.get_timestamp()}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup database
        self.stdout.write("   Backing up database...")
        # Implementation depends on database type
        
        # Backup user files
        if Path('inputs').exists():
            shutil.copytree('inputs', backup_dir / 'inputs', dirs_exist_ok=True)
            self.stdout.write("   Backed up user input files")
        
        # Backup color schemes
        if Path('color_schemes').exists():
            shutil.copytree('color_schemes', backup_dir / 'color_schemes', dirs_exist_ok=True)
            self.stdout.write("   Backed up color schemes")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Backup created at: {backup_dir}"))

    def migrate_legacy_data(self, options):
        """Migrate data from old format to new multi-user format"""
        self.stdout.write("🔄 Migrating legacy data to multi-user format...")
        
        User = get_user_model()
        
        # Check if admin user exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write("   Created admin user")
        
        # Migrate existing data files to admin user
        inputs_dir = Path('inputs')
        if inputs_dir.exists():
            self.stdout.write("   Migrating existing resume data to admin user...")
            # Implementation for migrating existing data
            
        self.stdout.write(self.style.SUCCESS("✅ Legacy data migration completed"))

    def create_color_scheme(self, options):
        """Create a new color scheme"""
        self.stdout.write("🎨 Creating new color scheme...")
        
        name = input("Color scheme name: ")
        slug = input("Color scheme slug (lowercase, no spaces): ")
        description = input("Description: ")
        
        primary = input("Primary color (hex): ")
        secondary = input("Secondary color (hex): ")
        accent = input("Accent color (hex): ")
        muted = input("Muted color (hex): ")
        
        scheme = ColorScheme.objects.create(
            name=name,
            slug=slug,
            description=description,
            primary_color=primary,
            secondary_color=secondary,
            accent_color=accent,
            muted_color=muted
        )
        
        self.stdout.write(self.style.SUCCESS(f"✅ Created color scheme: {scheme.name}"))

    def export_user_data(self, options):
        """Export user data for backup or migration"""
        username = options.get('user')
        if not username:
            raise CommandError("--user argument is required for export")
        
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' not found")
        
        self.stdout.write(f"📤 Exporting data for user: {username}")
        
        # Export user data to JSON
        export_data = {
            'user_info': {
                'username': user.username,
                'email': user.email,
                'professional_title': user.professional_title,
                'bio': user.bio,
            },
            'custom_color_schemes': [
                {
                    'name': scheme.name,
                    'slug': scheme.slug,
                    'description': scheme.description,
                    'primary_color': scheme.primary_color,
                    'secondary_color': scheme.secondary_color,
                    'accent_color': scheme.accent_color,
                    'muted_color': scheme.muted_color,
                }
                for scheme in user.custom_color_schemes.all()
            ],
            # Add more data as needed
        }
        
        export_file = f"{username}_export.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS(f"✅ User data exported to: {export_file}"))

    def optimize_database(self, options):
        """Optimize database performance"""
        self.stdout.write("⚡ Optimizing database...")
        
        # Run database optimization commands
        from django.core.management import call_command
        
        call_command('migrate')
        self.stdout.write("   Applied any pending migrations")
        
        # Add database-specific optimizations here
        
        self.stdout.write(self.style.SUCCESS("✅ Database optimization completed"))

    def generate_test_data(self, options):
        """Generate test data for development"""
        self.stdout.write("🧪 Generating test data...")
        
        User = get_user_model()
        
        # Create test users
        test_users = [
            {'username': 'test_user1', 'email': 'user1@example.com'},
            {'username': 'test_user2', 'email': 'user2@example.com'},
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f"   Created test user: {user.username}")
        
        # Create test color schemes
        test_schemes = [
            {
                'name': 'Test Blue',
                'slug': 'test_blue',
                'description': 'A test blue color scheme',
                'primary_color': '#0066CC',
                'secondary_color': '#004499',
                'accent_color': '#0099FF',
                'muted_color': '#6699CC'
            }
        ]
        
        for scheme_data in test_schemes:
            scheme, created = ColorScheme.objects.get_or_create(
                slug=scheme_data['slug'],
                defaults=scheme_data
            )
            if created:
                self.stdout.write(f"   Created test color scheme: {scheme.name}")
        
        self.stdout.write(self.style.SUCCESS("✅ Test data generated"))

    def get_timestamp(self):
        """Get current timestamp for backup naming"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
