"""
Main test module for Resume Generator

This module imports all test suites to ensure they're discovered by Django's test runner.
"""

# Import all test modules
from .test_models import *
from .test_services import *
from .test_api import *
