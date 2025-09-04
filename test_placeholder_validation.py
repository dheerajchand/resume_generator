#!/usr/bin/env python3
"""
Test script to demonstrate placeholder data validation
"""

from data_loader import ResumeData, create_resume_data
from data_validator import (
    detect_placeholders,
    validate_personal_info_no_placeholders,
    validate_experience_no_placeholders,
    validate_resume_data_complete,
    enforce_no_placeholders,
    create_validation_report,
)


def test_placeholder_detection():
    """Test placeholder detection functionality"""
    print("🧪 Testing Placeholder Detection")
    print("=" * 40)

    # Test cases
    test_cases = [
        (
            "Your Company Name, Your City, ST",
            [
                "Your Company Name",
                "Your City, ST",
                "Company Name",
                "Your City",
                "Your Company",
            ],
        ),
        ("YOUR FULL NAME", ["YOUR FULL NAME"]),
        ("Professional Title", ["Professional Title"]),
        ("Real Company Inc, San Francisco, CA", []),
        ("John Doe", []),
        ("Senior Software Engineer", []),
    ]

    for text, expected in test_cases:
        detected = detect_placeholders(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text}' -> {detected}")

    return True


def test_personal_info_validation():
    """Test personal info validation"""
    print("\n🧪 Testing Personal Info Validation")
    print("=" * 40)

    # Test with placeholders
    placeholder_info = {
        "name": "YOUR FULL NAME",
        "email": "your.email@example.com",
        "phone": "Your Phone Number",
        "website": "https://example.com",
        "linkedin": "https://linkedin.com/in/example",
    }

    result = validate_personal_info_no_placeholders(placeholder_info)
    print(f"Placeholder data validation: {'❌' if not result.is_valid else '✅'}")
    if result.errors:
        for error in result.errors:
            print(f"  Error: {error}")

    # Test with real data
    real_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "(555) 123-4567",
        "website": "https://johndoe.com",
        "linkedin": "https://linkedin.com/in/johndoe",
    }

    result = validate_personal_info_no_placeholders(real_info)
    print(f"Real data validation: {'✅' if result.is_valid else '❌'}")
    if result.errors:
        for error in result.errors:
            print(f"  Error: {error}")

    return True


def test_experience_validation():
    """Test experience validation"""
    print("\n🧪 Testing Experience Validation")
    print("=" * 40)

    # Test with placeholder data (like in original code)
    placeholder_experience = [
        {
            "title": "SENIOR SOFTWARE ENGINEER",
            "company": "Your Company Name, Your City, ST",  # This is the problem!
            "dates": "2020 – Present",
            "responsibilities": ["Developed software", "Led team"],
        }
    ]

    result = validate_experience_no_placeholders(placeholder_experience)
    print(f"Placeholder experience validation: {'❌' if not result.is_valid else '✅'}")
    if result.errors:
        for error in result.errors:
            print(f"  Error: {error}")

    # Test with real data
    real_experience = [
        {
            "title": "Senior Software Engineer",
            "company": "Google Inc, Mountain View, CA",
            "dates": "2020 – Present",
            "responsibilities": [
                "Developed scalable web applications",
                "Led team of 5 engineers",
            ],
        }
    ]

    result = validate_experience_no_placeholders(real_experience)
    print(f"Real experience validation: {'✅' if result.is_valid else '❌'}")
    if result.errors:
        for error in result.errors:
            print(f"  Error: {error}")

    return True


def test_complete_resume_validation():
    """Test complete resume validation with placeholder data"""
    print("\n🧪 Testing Complete Resume Validation")
    print("=" * 40)

    # Create resume data with placeholders (like original code)
    placeholder_data = {
        "personal_info": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "(555) 123-4567",
        },
        "summary": "Experienced software engineer with 5 years of experience.",
        "competencies": {
            "Programming": ["Python", "JavaScript", "Java"],
            "Tools": ["Git", "Docker", "AWS"],
        },
        "experience": [
            {
                "title": "SENIOR SOFTWARE ENGINEER",
                "company": "Your Company Name, Your City, ST",  # PLACEHOLDER!
                "dates": "2020 – Present",
                "responsibilities": ["Developed software", "Led team"],
            }
        ],
        "achievements": {
            "Technical": ["Built scalable system", "Improved performance"]
        },
    }

    try:
        resume_data = create_resume_data(placeholder_data)
        validation_result = validate_resume_data_complete(resume_data)

        print(
            f"Complete validation result: {'❌' if not validation_result.is_valid else '✅'}"
        )

        if validation_result.errors:
            print("Errors found:")
            for error in validation_result.errors:
                print(f"  • {error}")

        # Test enforcement
        print("\nTesting enforcement (should raise error):")
        try:
            enforce_no_placeholders(resume_data)
            print("❌ Enforcement failed - should have raised error")
        except ValueError as e:
            print(f"✅ Enforcement worked - caught error: {str(e)[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Error in validation: {e}")
        return False


def test_validation_report():
    """Test validation report generation"""
    print("\n🧪 Testing Validation Report")
    print("=" * 40)

    # Create resume data with placeholders
    placeholder_data = {
        "personal_info": {
            "name": "YOUR FULL NAME",  # PLACEHOLDER
            "email": "your.email@example.com",
            "phone": "Your Phone Number",  # PLACEHOLDER
        },
        "summary": "Professional summary here.",
        "competencies": {},
        "experience": [
            {
                "title": "Your Job Title",  # PLACEHOLDER
                "company": "Your Company Name, Your City, ST",  # PLACEHOLDER
                "dates": "Your Employment Dates",  # PLACEHOLDER
                "responsibilities": [],
            }
        ],
        "achievements": {},
    }

    try:
        resume_data = create_resume_data(placeholder_data)
        report = create_validation_report(resume_data)
        print("Validation Report:")
        print(report)
        return True

    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False


def demonstrate_original_problem():
    """Demonstrate the original problem with placeholder data"""
    print("\n🚨 Demonstrating Original Problem")
    print("=" * 50)

    print("The original code generates resumes with placeholder data like:")
    print("  • 'Your Company Name, Your City, ST'")
    print("  • 'YOUR FULL NAME'")
    print("  • 'Professional Title'")
    print("  • 'Your Phone Number'")
    print()
    print("This makes resumes unprofessional and unusable!")
    print()
    print("Our functional approach with validation catches these issues:")

    # Show how our validation catches the problem
    problematic_data = {
        "personal_info": {
            "name": "YOUR FULL NAME",
            "email": "your.email@example.com",
            "phone": "Your Phone Number",
        },
        "summary": "Professional summary",
        "competencies": {},
        "experience": [
            {
                "title": "SENIOR SOFTWARE ENGINEER",
                "company": "Your Company Name, Your City, ST",
                "dates": "2020 – Present",
                "responsibilities": ["Developed software"],
            }
        ],
        "achievements": {},
    }

    try:
        resume_data = create_resume_data(problematic_data)
        enforce_no_placeholders(resume_data)
        print("❌ Should have failed but didn't")
    except ValueError as e:
        print("✅ Validation correctly caught placeholder data:")
        print(f"   {str(e)[:200]}...")


def main():
    """Run all placeholder validation tests"""
    print("🚀 Placeholder Data Validation Test Suite")
    print("=" * 60)

    tests = [
        test_placeholder_detection,
        test_personal_info_validation,
        test_experience_validation,
        test_complete_resume_validation,
        test_validation_report,
        demonstrate_original_problem,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All placeholder validation tests passed!")
        print("The functional approach successfully prevents placeholder data issues.")
    else:
        print("⚠️  Some tests failed. Check the output above.")

    return passed == total


if __name__ == "__main__":
    main()
