#!/usr/bin/env python3
"""
Test script to demonstrate functional approach
"""

import json
from pathlib import Path
from data_loader import load_resume_data, load_config_data, get_default_config
from style_generator import create_all_styles


def test_data_loading():
    """Test the functional data loading approach"""
    print("🧪 Testing Functional Data Loading")
    print("=" * 40)
    
    # Test with existing data
    data_file = "inputs/dheeraj_chand_software_engineer/resume_data.json"
    config_file = "inputs/dheeraj_chand_software_engineer/config.json"
    
    try:
        # Load resume data
        resume_data = load_resume_data(data_file)
        print(f"✅ Loaded resume data for: {resume_data.personal_info['name']}")
        print(f"   Experience entries: {len(resume_data.experience)}")
        print(f"   Competency categories: {len(resume_data.competencies)}")
        
        # Load config data
        config_data = load_config_data(config_file)
        print(f"✅ Loaded config with {len(config_data.colors)} colors")
        print(f"   Color scheme: {config_data.metadata.get('scheme_name', 'unknown')}")
        
        # Create styles
        styles = create_all_styles(config_data)
        print(f"✅ Created {len(styles)} paragraph styles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_default_config():
    """Test default configuration creation"""
    print("\n🧪 Testing Default Configuration")
    print("=" * 40)
    
    try:
        default_config = get_default_config()
        print(f"✅ Created default config with {len(default_config.colors)} colors")
        print(f"   Default name color: {default_config.colors['NAME_COLOR']}")
        print(f"   Default font: {default_config.typography['FONT_MAIN']}")
        
        # Create styles from default config
        styles = create_all_styles(default_config)
        print(f"✅ Created {len(styles)} styles from default config")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_validation():
    """Test data validation"""
    print("\n🧪 Testing Data Validation")
    print("=" * 40)
    
    # Test valid data
    valid_data = {
        'personal_info': {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '123-456-7890'
        },
        'summary': 'Test summary',
        'competencies': {
            'Programming': ['Python', 'JavaScript'],
            'Tools': ['Git', 'Docker']
        },
        'experience': [
            {
                'title': 'Software Engineer',
                'company': 'Test Company',
                'dates': '2020-2023',
                'responsibilities': ['Developed software', 'Led team']
            }
        ],
        'achievements': {
            'Technical': ['Built system', 'Optimized performance']
        }
    }
    
    try:
        from data_loader import create_resume_data
        resume_data = create_resume_data(valid_data)
        print(f"✅ Valid data processed successfully")
        print(f"   Name: {resume_data.personal_info['name']}")
        print(f"   Competencies: {len(resume_data.competencies)} categories")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_invalid_data():
    """Test handling of invalid data"""
    print("\n🧪 Testing Invalid Data Handling")
    print("=" * 40)
    
    # Test missing required fields
    invalid_data = {
        'personal_info': {
            'name': 'Test User'
            # Missing required email field
        },
        'summary': 'Test summary'
    }
    
    try:
        from data_loader import create_resume_data
        resume_data = create_resume_data(invalid_data)
        print("❌ Should have failed with missing email")
        return False
        
    except ValueError as e:
        print(f"✅ Correctly caught validation error: {e}")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Functional Approach Test Suite")
    print("=" * 50)
    
    tests = [
        test_data_loading,
        test_default_config,
        test_validation,
        test_invalid_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Functional approach is working.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    main()
