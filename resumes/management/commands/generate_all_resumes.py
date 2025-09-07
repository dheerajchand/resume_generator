#!/usr/bin/env python3
"""
Django management command to generate all resume combinations
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from resumes.core_services import ResumeManager
import os


class Command(BaseCommand):
    help = 'Generate all resume combinations (nuclear option)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='outputs',
            help='Output directory for generated resumes'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Skip confirmation prompt'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force generation without confirmation (same as --confirm)'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        confirm = options['confirm'] or options['force']
        
        # Calculate total combinations
        manager = ResumeManager()
        total_combinations = (
            len(manager.versions) * 
            len(manager.length_variants) *
            len(manager.color_schemes) * 
            len(manager.formats)
        )
        
        self.stdout.write(
            self.style.SUCCESS('☢️  NUCLEAR OPTION: Generating EVERYTHING')
        )
        self.stdout.write('=' * 60)
        self.stdout.write(
            f'📊 Total combinations: {len(manager.versions)} versions × '
            f'{len(manager.length_variants)} lengths × '
            f'{len(manager.formats)} formats × {len(manager.color_schemes)} color schemes'
        )
        self.stdout.write(f'🎯 Total files to generate: {total_combinations}')
        self.stdout.write('')
        self.stdout.write('⏰ This will take several minutes...')
        self.stdout.write('☕ Perfect time for a coffee break!')
        self.stdout.write('')
        
        if not confirm:
            response = input('🤔 Are you sure you want to generate ALL resumes with ALL color schemes? (y/N): ')
            if response.lower() != 'y':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return
        
        self.stdout.write('🚀 Launching nuclear generation sequence...')
        self.stdout.write('=' * 60)
        
        # Generate all combinations
        results = manager.generate_all_combinations(output_dir)
        
        self.stdout.write('')
        self.stdout.write('☢️  NUCLEAR GENERATION COMPLETE!')
        self.stdout.write('=' * 60)
        self.stdout.write(f'✅ Successfully generated: {results["success"]} files')
        self.stdout.write(f'❌ Failed: {results["failed"]} files')
        
        if results["failed"] == 0:
            success_rate = 100.0
        else:
            success_rate = (results["success"] / total_combinations) * 100
        
        self.stdout.write(f'📊 Success rate: {success_rate:.1f}%')
        self.stdout.write('')
        self.stdout.write(f'📁 Find your nuclear arsenal in the {output_dir}/ directory!')
        self.stdout.write('   Organized by: outputs/[version]/[color_scheme]/[format]/')
        self.stdout.write('   Files named: dheeraj_chand_[version]_[color_scheme].[extension]')
