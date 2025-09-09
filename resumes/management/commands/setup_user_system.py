"""
Management command to set up user system and migrate existing resume data
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from resumes.models import UserProfile, UserDirectory, UserResumeData, ColorScheme
import os
import json
import shutil
from pathlib import Path

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up user system and migrate existing resume data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to set up (default: admin)',
            default='admin'
        )
        parser.add_argument(
            '--migrate-existing',
            action='store_true',
            help='Migrate existing resume data to user system'
        )

    def handle(self, *args, **options):
        username = options['username']
        migrate_existing = options['migrate_existing']

        try:
            # Get or create user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {username}')
                )

            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'professional_summary': 'Professional with expertise in data analysis, research, and software development.',
                    'default_resume_template': 'comprehensive',
                    'auto_generate_on_update': True,
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for: {username}')
                )

            # Create user directories
            base_dir = Path('user_data')
            user_dir = base_dir / username
            input_dir = user_dir / 'inputs'
            output_dir = user_dir / 'outputs'

            directory, created = UserDirectory.objects.get_or_create(
                user=user,
                defaults={
                    'input_directory': str(input_dir),
                    'output_directory': str(output_dir),
                }
            )

            if created:
                # Initialize directories
                directory.initialize_directories()
                self.stdout.write(
                    self.style.SUCCESS(f'Created directories for: {username}')
                )

            # Create color schemes if they don't exist
            self.create_color_schemes()

            # Migrate existing resume data if requested
            if migrate_existing:
                self.migrate_existing_data(user, input_dir, output_dir)

            self.stdout.write(
                self.style.SUCCESS('User system setup completed successfully!')
            )

        except Exception as e:
            raise CommandError(f'Error setting up user system: {e}')

    def create_color_schemes(self):
        """Create color schemes from existing JSON files"""
        color_schemes_dir = Path('color_schemes')
        
        if not color_schemes_dir.exists():
            self.stdout.write(
                self.style.WARNING('Color schemes directory not found, skipping...')
            )
            return

        for scheme_file in color_schemes_dir.glob('*.json'):
            scheme_name = scheme_file.stem
            
            # Skip if scheme already exists
            if ColorScheme.objects.filter(name=scheme_name).exists():
                continue

            try:
                with open(scheme_file, 'r') as f:
                    colors = json.load(f)

                ColorScheme.objects.create(
                    name=scheme_name,
                    description=f'Color scheme: {scheme_name}',
                    colors=colors,
                    is_default=(scheme_name == 'default_professional'),
                    is_active=True
                )

                self.stdout.write(
                    self.style.SUCCESS(f'Created color scheme: {scheme_name}')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating color scheme {scheme_name}: {e}')
                )

    def migrate_existing_data(self, user, input_dir, output_dir):
        """Migrate existing resume data to user system"""
        existing_inputs = Path('inputs')
        
        if not existing_inputs.exists():
            self.stdout.write(
                self.style.WARNING('No existing inputs directory found, skipping migration...')
            )
            return

        # Create user input directory structure
        os.makedirs(input_dir, exist_ok=True)

        # Copy existing resume data files
        for resume_dir in existing_inputs.iterdir():
            if resume_dir.is_dir() and resume_dir.name.startswith('dheeraj_chand_'):
                # Determine resume type and length variant
                name_parts = resume_dir.name.split('_')
                
                if len(name_parts) >= 4:
                    resume_type = '_'.join(name_parts[2:-1]) if 'abbreviated' in resume_dir.name else '_'.join(name_parts[2:])
                    length_variant = 'short' if 'abbreviated' in resume_dir.name else 'long'
                else:
                    resume_type = 'comprehensive'
                    length_variant = 'long'

                # Create user-specific resume data
                resume_data, created = UserResumeData.objects.get_or_create(
                    user=user,
                    resume_type=resume_type,
                    length_variant=length_variant,
                    defaults={
                        'input_file_path': str(resume_dir),
                        'output_directory': str(output_dir),
                        'is_active': True,
                    }
                )

                if created:
                    # Load and store resume content
                    resume_file = resume_dir / 'resume_data.json'
                    if resume_file.exists():
                        try:
                            with open(resume_file, 'r') as f:
                                content = json.load(f)
                            
                            resume_data.personal_info = content.get('personal_info', {})
                            resume_data.summary = content.get('summary', '')
                            resume_data.competencies = content.get('competencies', {})
                            resume_data.experience = content.get('experience', [])
                            resume_data.achievements = content.get('achievements', {})
                            resume_data.education = content.get('education', [])
                            resume_data.projects = content.get('projects', [])
                            resume_data.certifications = content.get('certifications', [])
                            resume_data.additional_info = content.get('additional_info', '')
                            resume_data.save()

                            self.stdout.write(
                                self.style.SUCCESS(f'Migrated: {resume_type} ({length_variant})')
                            )

                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'Error migrating {resume_dir.name}: {e}')
                            )

        # Copy existing outputs if they exist
        existing_outputs = Path('outputs')
        if existing_outputs.exists():
            try:
                # Copy outputs to user directory
                shutil.copytree(existing_outputs, output_dir, dirs_exist_ok=True)
                self.stdout.write(
                    self.style.SUCCESS('Copied existing outputs to user directory')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error copying outputs: {e}')
                )

