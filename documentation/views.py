#!/usr/bin/env python3
"""
Documentation Views
Serves documentation pages as static web pages
"""

from django.shortcuts import render
from django.http import Http404
from pathlib import Path
import os


def docs_index(request):
    """Main documentation index page"""
    context = {
        'title': 'Documentation',
        'description': 'Complete documentation for the Resume Generator system',
        'docs': [
            {
                'title': 'Getting Started',
                'description': 'Complete setup guide from zero to working system',
                'url': 'getting-started',
                'audience': 'Absolute beginners',
                'length': '15-30 minutes',
                'icon': '🚀'
            },
            {
                'title': 'User Manual',
                'description': 'Learn all features and create professional resumes',
                'url': 'user-manual',
                'audience': 'End users',
                'length': '20-30 minutes',
                'icon': '📖'
            },
            {
                'title': 'Developer Guide',
                'description': 'Technical details for developers and advanced users',
                'url': 'developer-guide',
                'audience': 'Developers',
                'length': '45-60 minutes',
                'icon': '⚙️'
            },
            {
                'title': 'API Documentation',
                'description': 'Complete API reference for programmatic access',
                'url': 'api-documentation',
                'audience': 'Developers',
                'length': '30-45 minutes',
                'icon': '🔌'
            },
            {
                'title': 'ReportLab Template Guide',
                'description': 'Understand and customize the PDF template system',
                'url': 'reportlab-template-guide',
                'audience': 'Developers',
                'length': '30-45 minutes',
                'icon': '📄'
            },
            {
                'title': 'Color Schemes Guide',
                'description': 'Create and customize professional color schemes',
                'url': 'color-schemes-guide',
                'audience': 'Designers',
                'length': '25-35 minutes',
                'icon': '🎨'
            },
            {
                'title': 'Troubleshooting',
                'description': 'Fix common problems and issues',
                'url': 'troubleshooting',
                'audience': 'Everyone',
                'length': '15-20 minutes',
                'icon': '🔧'
            },
            {
                'title': 'FAQ',
                'description': 'Frequently asked questions and answers',
                'url': 'faq',
                'audience': 'Everyone',
                'length': '10-15 minutes',
                'icon': '❓'
            },
            {
                'title': 'Examples',
                'description': 'Real-world examples and templates',
                'url': 'examples',
                'audience': 'Everyone',
                'length': '20-30 minutes',
                'icon': '💡'
            }
        ]
    }
    return render(request, 'documentation/index.html', context)


def docs_page(request, page_name):
    """Serve individual documentation pages"""
    
    # Map page names to file names
    page_mapping = {
        'getting-started': 'getting-started.md',
        'user-manual': 'user-manual.md',
        'developer-guide': 'developer-guide.md',
        'api-documentation': 'api-documentation.md',
        'reportlab-template-guide': 'reportlab-template-guide.md',
        'color-schemes-guide': 'color-schemes-guide.md',
        'troubleshooting': 'troubleshooting.md',
        'faq': 'faq.md',
        'examples': 'examples.md',
        'complete-summary': 'COMPLETE_DOCUMENTATION_SUMMARY.md'
    }
    
    if page_name not in page_mapping:
        raise Http404("Documentation page not found")
    
    # Get the markdown file path
    docs_dir = Path(__file__).parent.parent / 'docs'
    md_file = docs_dir / page_mapping[page_name]
    
    if not md_file.exists():
        raise Http404("Documentation file not found")
    
    # Read the markdown content
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise Http404(f"Error reading documentation: {e}")
    
    # Get page metadata
    page_metadata = {
        'getting-started': {
            'title': 'Getting Started Guide',
            'description': 'Complete setup guide from zero to working system',
            'icon': '🚀'
        },
        'user-manual': {
            'title': 'User Manual',
            'description': 'Learn all features and create professional resumes',
            'icon': '📖'
        },
        'developer-guide': {
            'title': 'Developer Guide',
            'description': 'Technical details for developers and advanced users',
            'icon': '⚙️'
        },
        'api-documentation': {
            'title': 'API Documentation',
            'description': 'Complete API reference for programmatic access',
            'icon': '🔌'
        },
        'reportlab-template-guide': {
            'title': 'ReportLab Template Guide',
            'description': 'Understand and customize the PDF template system',
            'icon': '📄'
        },
        'color-schemes-guide': {
            'title': 'Color Schemes Guide',
            'description': 'Create and customize professional color schemes',
            'icon': '🎨'
        },
        'troubleshooting': {
            'title': 'Troubleshooting Guide',
            'description': 'Fix common problems and issues',
            'icon': '🔧'
        },
        'faq': {
            'title': 'Frequently Asked Questions',
            'description': 'Common questions and answers',
            'icon': '❓'
        },
        'examples': {
            'title': 'Examples and Templates',
            'description': 'Real-world examples and copy-paste templates',
            'icon': '💡'
        },
        'complete-summary': {
            'title': 'Complete Documentation Summary',
            'description': 'Overview of all available documentation',
            'icon': '📚'
        }
    }
    
    metadata = page_metadata.get(page_name, {
        'title': page_name.replace('-', ' ').title(),
        'description': 'Documentation page',
        'icon': '📄'
    })
    
    context = {
        'title': metadata['title'],
        'description': metadata['description'],
        'icon': metadata['icon'],
        'content': content,
        'page_name': page_name
    }
    
    return render(request, 'documentation/page.html', context)


def docs_search(request):
    """Search documentation pages"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'documentation/search.html', {
            'title': 'Search Documentation',
            'query': '',
            'results': []
        })
    
    # Search through documentation files
    docs_dir = Path(__file__).parent.parent / 'docs'
    results = []
    
    for md_file in docs_dir.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Simple search (case-insensitive)
            if query.lower() in content.lower():
                # Get first few lines as preview
                lines = content.split('\n')[:5]
                preview = ' '.join(lines).strip()[:200] + '...' if len(' '.join(lines)) > 200 else ' '.join(lines)
                
                # Map filename to page name
                page_name = md_file.stem.replace('_', '-').lower()
                if page_name == 'complete-documentation-summary':
                    page_name = 'complete-summary'
                
                results.append({
                    'title': md_file.stem.replace('_', ' ').title(),
                    'preview': preview,
                    'url': f'/docs/{page_name}/',
                    'filename': md_file.name
                })
                
        except Exception as e:
            continue
    
    context = {
        'title': 'Search Documentation',
        'query': query,
        'results': results
    }
    
    return render(request, 'documentation/search.html', context)